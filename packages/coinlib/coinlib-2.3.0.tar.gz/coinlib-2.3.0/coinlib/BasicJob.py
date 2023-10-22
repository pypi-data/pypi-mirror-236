import math

import aio_pika
import numpy as np
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from coinlib import helper, Registrar
from coinlib.BasicJobSessionStorage import BasicJobSessionStorage, LastSignalValue
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.data.DataTable import DataTable, LastEntry
from coinlib.helper import serializeDTO, to_trendline, trendline
from coinlib.feature.FeatureDTO import RabbitInfo
import pandas as pd
from dateutil import parser
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import datetime
from operator import is_not
from functools import partial
from enum import Enum

class CrossMode(Enum):
    up=1
    down=2
    both=3


class BasicJob:
    def __init__(self, table: DataTable, inputs, storageManager = None):
        self.table = table
        if storageManager is None:
            storageManager = BasicJobSessionStorage()
        self._df = self.table.getDf()
        self.df = self.table.getDf()
        self.registrar = Registrar()
        self._storageManager = storageManager
        self._storageManager.setCurrentIndex(self.closeDate())
        self.inputs = inputs
        self.uniqueName = ""
        self._sessionInfo = self._storageManager.getStorage()
        self.features = self

        ## gets a signal data

    def getStub(self) -> stats.DataWorkerStub:
        pass

    def getWorker(self) -> WorkerJobProcess:
        pass

    def set(self, name, data, index=None):

        return self.table.setColumn(name, data, index)

    def getOutputCol(self):
        return "result"

    def result(self, resultList, colname=None, fillType="front", type=float):

        #if isinstance(resultList, np.ndarray):
        #    resultList = np.pad(resultList, (self.df.shape[0] - len(resultList), 0), 'constant', constant_values=(np.nan))

        #self.df[self.getOutputCol()] = resultList
        self.table.setColumn(self.getOutputCol(), resultList, pad=True, type=type)

        return self.table.column(self.getOutputCol())

    def lastIndexOf(self, name, operator, value, tickDistance=None):
        if type(name) == str:
            name = self.get(name, limit=tickDistance)

        ret = False
        if operator == "<":
            i = 0
            for d in name:
                if d < value:
                    ret = i
                i = i + 1
        if operator == "<=":
            i = 0
            for d in name:
                if d <= value:
                    ret = i
                i = i + 1
        if operator == ">":
            i = 0
            for d in name:
                if d > value:
                    ret = i
                i = i + 1
        if operator == ">=":
            i = 0
            for d in name:
                if d >= value:
                    ret = i
                i = i + 1
        if operator == "==":
            i = 0
            for d in name:
                if d == value:
                    ret = i
                i = i + 1

        return ret


    def was(self, name, operator, value, tickDistance, stable=False, stableValue=None, stableLength=2):
        ret = False
        list1 = self.get(name, limit=tickDistance)

        index = self.lastIndexOf(list1, operator, value, tickDistance=tickDistance)

        if index is not False:

            list1 = list1[index:]
            ret = True

            if stable:
                if operator == "<":
                    ret = [x < stableValue for x in list1].count(True) >= stableLength
                if operator == "<=":
                    ret = [x <= stableValue for x in list1].count(True) >= stableLength
                if operator == ">":
                    ret = [x > stableValue for x in list1].count(True) >= stableLength
                if operator == ">=":
                    ret = [x >= stableValue for x in list1].count(True) >= stableLength
                if operator == "==":
                    ret = [x == stableValue for x in list1].count(True) >= stableLength

        return ret

    ## This method adds a signal
    def wasSignal(self, name, maxSecondsDistance=0, minSecondsDistance=0, logicId=None):
        lastValue = self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(), name)

        if lastValue.found is True:
            if minSecondsDistance > 0:
                if lastValue.distanceSeconds > minSecondsDistance:
                    return True
            if maxSecondsDistance > 0:
                if lastValue.distanceSeconds < maxSecondsDistance:
                    return True

        return False

    ## This method adds a signal
    def lastSignal(self, name, logicId=None, maxSecondsDistance=None) -> LastSignalValue:

        return self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(),
                                                  name, maxSecondsDistance=maxSecondsDistance)

    def deleteSignal(self, name):

        return self._storageManager.deleteSignall(name)

    ## This method adds a signal
    def signal(self, name, data=None, index=-1, logicId=None) -> LastSignalValue:

        if not (isinstance(data, str) or isinstance(data, float) or isinstance(data, int) or data is None):
            raise Exception("For signal data only string, float or int is allowed.")

        if data is not None:
            return self._storageManager.setSignal(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getSignal(logicId if logicId is not None else self.getUniqueName(), name)

    def getInputValue(self, input):

        if isinstance(input, dict):
            if "value" in input:
                return input["value"]

        return input


    def getNow(self, name):
        return self.current(name)


    def is_new_day(self, i=-1, offset=0):
        if i == 0:
            return False
        dt1 = self.table.index[i] + datetime.timedelta(hours=offset)
        dt2 = self.table.index[i-1] + datetime.timedelta(hours=offset)
        # check if there is a new day between the two dates
        return (dt1.day != dt2.day)

    def is_new_week(self, i=-1, offset=0):
        if i == 0:
            return False
        dt1 = self.table.index[i] + datetime.timedelta(hours=offset)
        dt2 = self.table.index[i-1] + datetime.timedelta(hours=offset)
        # check if there is a new week between the two dates
        return (dt1.week != dt2.week)

    def getCurrent(self, name):
        return self.current(name)

    def logger(self):
        return self.registrar.logger

    def functions(self):
        worker = self.getWorker()

        return worker.getIndicators()

    def isOfflineMode(self):
        worker = self.getWorker()

        return worker.isOfflineWorker()

    def getTrendlines(self, name, history_in_sec=None):
        """
        This method returns you all the trendlines that are currently "in your time" (So the
        trendlines that are going minimum to current position - history_in_sec)
        """
        trendlines = self.get(name)

        if trendlines is not None:

            trendlines = trendlines[trendlines != np.array(None)]
            trendlines = [to_trendline(x) for x in trendlines]

            if len(trendlines) > 0:
                date = self.date()

                if history_in_sec is not None:
                    date = date - datetime.timedelta(seconds=history_in_sec)

                found_lines = []
                for t in trendlines:

                    if t["x1"] > date:
                        found_lines.append(t)


                return found_lines

        return []

    ####
    def crossline_up(self, d1, d2):
        return self.crossline(d1, d2, mode=CrossMode.up)

    def crossline_down(self, d1, d2):
        return self.crossline(d1, d2, mode=CrossMode.down)

    def crossline(self, d1, d2, mode=CrossMode.both):
        if type(d1) == str:
            d1 = self.get(d1, with_dates=True)
        if type(d2) == str:
            d2 = self.get(d2, with_dates=True)

        if len(d2["data"]) < len(d1["data"]):
            marker = d2
            dataline = d1
        if len(d1["data"]) < len(d2["data"]):
            marker = d1
            dataline = d2

        if len(marker["data"]) > 1:
            line_grad = marker["data"][-2:]
            l1 = line_grad[-2]
            l2 = line_grad[-1]
            t1 = marker["datetime"][-2]
            t2 = marker["datetime"][-1]
            tdelta = int((t2.timestamp() - t1.timestamp()))
            ldelta = l2 - l1
            m = ldelta / tdelta

            y = (m * int(dataline["datetime"][-1].timestamp() - t2.timestamp())) + l2

            currentline = dataline["data"]

            if mode == CrossMode.both or mode == CrossMode.up:
                if currentline[-1] > y:
                    return True
            if mode == CrossMode.both or mode == CrossMode.down:
                if currentline[-1] < y:
                    return True

        return False

    def isDateGreater(self, date, time=None):
        formatter = "%Y-%m-%d"
        if time is not None:
            date = date +" "+ time
            formatter = formatter + " %H:%M:%S"

        curdate = self.date(index=-1)
        testdate = datetime.datetime.fromisoformat(date)
        if testdate is None:
            raise(Exception("The date u gave can not be parsed to a date."))

        if curdate > testdate:
            return True
        return False

    def isDate(self, date, time=None):
        if time is not None:
            date = date +" "+ time

        curdate = self.date(index=-1)
        lastdate = self.date(index=-3)
        testdate = parser.parse(date)
        if testdate is None:
            raise(Exception("The date u gave can not be parsed to a date."))


        if curdate >= testdate >= lastdate:
            return True
        return False


    def isMarker(self):
        marker = self.get("marker", -1)

        if not pd.isna(marker):
            return True
        return False

    def cross_up_stable(self, line1, line2, index):
        return self.cross_stable(line1, line2, mode=CrossMode.up, index=index)
    def cross_down_stable(self, line1, line2, index):
        return self.cross_stable(line1, line2, mode=CrossMode.down, index=index)
    def cross_stable(self, line1, line2, index, mode=CrossMode):
        return self.cross(line1, line2, mode=mode, index=index, keptStable=True)
    def cross_down(self, line1, line2, index=-1):
        return self.cross(line1, line2, mode=CrossMode.down, index=index)
    def cross_up(self, line1, line2, index=-1):
        return self.cross(line1, line2, mode=CrossMode.up, index=index)
    def cross(self, line1, line2, mode=CrossMode, index=-1, keptStable=False):
        """
        This method calculates a cross between 2 lines.  (line1 X line2).

        mode = Mode can be up, down, both
        index = How far away from now should we search - default is "-1" than the cross is straight here
        keptStable = Checks if there was a cross and the data kept stable on that side
        """

        if index > 0:
            index = -index
        crossFound = None
        wasStable = 0
        i = index
        while i < 0:

            d1 = self.get(line1, index=i)
            d2 = self.get(line2, index=i)
            d1_1 = self.get(line1, index=-1+i)
            d2_2 = self.get(line2, index=-1+i)

            if d1 is None or d2 is None or d1_1 is None or d2_2 is None:
                pass
            else:
                if crossFound is None or keptStable is False:
                    if mode == CrossMode.up or mode == CrossMode.both:
                        if d1_1 < d2_2 and d1 > d2:
                            crossFound = i
                            wasStable = 0
                            direction = CrossMode.up
                            if keptStable is False:
                                return direction
                            continue
                    if mode == CrossMode.down or mode == CrossMode.both:
                        if d1_1 > d2_2 and d1 < d2:
                            crossFound = i
                            wasStable = 0
                            direction = CrossMode.down
                            if keptStable is False:
                                return direction
                            continue

                if crossFound is not None and keptStable is True:
                    if direction == CrossMode.down:
                        if d1 > d2:
                            crossFound = None
                            i = i - 1
                            wasStable = 0
                        else:
                            wasStable = wasStable + 1
                    if direction == CrossMode.up:
                        if d1 < d2:
                            wasStable = 0
                            i = i - 1
                            crossFound = None
                        else:
                            wasStable = wasStable + 1


            i = i + 1

        if keptStable is False:
            if crossFound is not None:
                return direction
        else:
            if crossFound is not None and wasStable >= (-index-1):
                return direction

        return False

    def is_set(self, data_or_name):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name, index=-1)

        if data_or_name is None:
            return None

        return data_or_name is not None and not np.isnan(data_or_name)

    def higher_than(self, data_or_name, lower_name_or_value):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name, index=-1)

        if data_or_name is None:
            return None

        if type(lower_name_or_value) == str:
            lower_name_or_value = self.get(lower_name_or_value, index=-1)

        if data_or_name is None or  np.isnan(data_or_name) or lower_name_or_value is None or np.isnan(lower_name_or_value):
            return False

        return data_or_name > lower_name_or_value

    def lower_than(self, data_or_name, lower_name_or_value):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name, index=-1)
        if data_or_name is None:
            return None

        if type(lower_name_or_value) == str:
            lower_name_or_value = self.get(lower_name_or_value, index=-1)

        if data_or_name is None or  np.isnan(data_or_name) or lower_name_or_value is None or np.isnan(lower_name_or_value):
            return False

        return data_or_name < lower_name_or_value

    def grad(self, data_or_name, length=1):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name)
        if data_or_name is None:
            return None
        if "data" in data_or_name:
            data_or_name = data_or_name["data"]
        arr = data_or_name
        ret_Data = np.array([((arr[-i] / arr[-i - 1])-1)*100 for i in range(1, length+1)])

        if length is not None:
            if len(ret_Data) > 0:
                return ret_Data[-1]
            else:
                return None

        return ret_Data

    def get_all(self, name, filterNone = False, replaceNone=None, limit=None,
            keepPaddingNones=False, with_dates=False, clear_nan=True, to_date=None, from_date=None):
        return self.get(name, index=None, filterNone=filterNone, replaceNone=replaceNone, limit=limit,
                        keepPaddingNones=keepPaddingNones, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date,
                        from_date=from_date)
    def getAll(self, name, filterNone = False, replaceNone=None, limit=None,
            keepPaddingNones=False, with_dates=False, clear_nan=True, to_date=None, from_date=None):
        return self.get(name, index=None, filterNone=filterNone, replaceNone=replaceNone, limit=limit,
                        keepPaddingNones=keepPaddingNones, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date,
                        from_date=from_date)


    def hasIncreased(self, data_or_name, from_date=None):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name, from_date=from_date)

        if data_or_name is None:
            return None

        if data_or_name is not None:
            for i in range(1, len(data_or_name)):
                if data_or_name[i] < data_or_name[i-1]:
                    return False

        return True

    def hasDecreased(self, data_or_name, from_date=None):
        if type(data_or_name) == str:
            data_or_name = self.get(data_or_name, from_date=from_date)

        if data_or_name is None:
            return None

        if data_or_name is not None:
            for i in range(len(data_or_name)-1, 0, -1):
                if data_or_name[i] > data_or_name[i-1]:
                    return False

        return True

    def getMoments(self, name, limit=None):
        data = self.get(name, index=None, filterNone=False, replaceNone=None, limit=limit,
                        keepPaddingNones=False, with_dates=True, clear_nan=True)
        relevantData = []
        for i in range(len(data["data"])-1, 0, -1):
            if data["data"][i] is not None and pd.notna(data["data"][i]):
                d = data["datetime"][i]
                current_date = self.date()
                distance = current_date - d
                relevantData.append({
                    "date": d,
                    "value": data["data"][i],
                    "distance_index": math.floor(distance.seconds/60) if distance.seconds > 0 else 0,
                    "distance": distance
                })
        relevantData.reverse()
        return relevantData

    def subtract(self, data_or_name1, data_or_name2):
        if type(data_or_name1) == str:
            data_or_name1 = self.get(data_or_name1)
        if type(data_or_name2) == str:
            data_or_name2 = self.get(data_or_name2)

        if len(data_or_name1) > len(data_or_name2):
            data_or_name1 = data_or_name1[len(data_or_name1)-len(data_or_name2):]
        elif len(data_or_name1) < len(data_or_name2):
            data_or_name2 = data_or_name2[len(data_or_name2)-len(data_or_name1):]

        return data_or_name1 - data_or_name2


    def get(self, name, index=None, filterNone = False, replaceNone=None, limit=None,
            keepPaddingNones=False, with_dates=False, clear_nan=True, to_date=None, from_date=None):

        # if the name is a number, so we return it directly
        if type(name) == int or type(name) == float:
            return name

        data = None
        try:
                maybe_col_name = name
                child_col_name = ""
                if ":" in maybe_col_name:
                    maybe_col_name = maybe_col_name.split(":")[0]
                    child_col_name = ":"+name.split(":")[1]

                # if its a key of inputs - lets export the right column
                if maybe_col_name in self.inputs:
                    if isinstance(self.inputs[maybe_col_name], str):
                        return self.get(self.getInputValue(self.inputs[maybe_col_name])+child_col_name, index, filterNone, replaceNone, limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                    if self.inputs[maybe_col_name]["type"] == "dataInput":
                        return self.get(self.getInputValue(self.inputs[maybe_col_name]["value"])+child_col_name, index, filterNone, replaceNone, limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)

                data = None
                if name in self.table.columns:
                    data = self.table.column(name, index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif maybe_col_name + ":y" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":y", index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif maybe_col_name + ":marker" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":marker", index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif "additionalData."+maybe_col_name in self.table.columns:
                    data = self.table.column("additionalData."+maybe_col_name, index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif maybe_col_name + ":close" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":close", index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif "stats."+maybe_col_name in self.table.columns:
                    data = self.table.column("stats."+maybe_col_name, index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif "stats." + name in self.table.columns:
                    data = self.table.column("stats." + name, index, limit=limit, with_dates=with_dates, clear_nan=clear_nan, to_date=to_date, from_date=from_date)
                elif maybe_col_name in self.inputs:
                    data = self.inputs[name]
        except Exception as e:
            self.logger().error(e)

            if name != "main" and not name.startswith("chart"):
                raise Exception("The name of your attributes should normally start with chartXX.")

        if data is not None and (filterNone or replaceNone):
            if isinstance(data, list) or isinstance(data, (np.ndarray, np.generic)):
                if len(data) > 1:
                    data = [i if i is not None and (((type(i) != str and not np.isnan(i)) or
                                  (type(i) == str and len(i) > 0))) else None for i in data]
                    if filterNone is True:
                        data = [i for i in data if i is not None]
                    if replaceNone is not None:
                        data = [0 if i is None else i for i in data]
                else:
                    return data[0]
            else:
                if np.isnan(data):
                    data = None

        if data is not None and not keepPaddingNones:
            dataElement = data
            if with_dates:
                dataElement = data["data"]
            if not isinstance(dataElement, pd.DataFrame) and not isinstance(dataElement, pd.Series) \
                    and type(data) != float and type(data) != str:
                start, end = 0, len(data)
                for x in range(len(dataElement)):
                    if self.isValNotEmpty(dataElement[x]):
                        if len(dataElement) > x+1 and self.isValNotEmpty(dataElement[x+1]):
                            start = x
                            break
                if with_dates:
                    data["data"] = dataElement[start:]
                    data["datetime"] = data["datetime"][start:]
                else:
                    data = dataElement[start:]

        return data

    def getAsCandle(self, name, index=None) -> {"open": [], "high": [], "low": [], "close": [], "volume": []}:

        data = {
            "open": self.getAsArray(name+":open", index),
            "high": self.getAsArray(name+":high", index),
            "low": self.getAsArray(name+":low", index),
            "close": self.getAsArray(name+":close", index),
            "volume": self.getAsArray(name+":volume", index),
        }

        return data

    def isValNotEmpty(self, e):
        try:
            if type(e) == int or isinstance(e, np.floating) or type(e) == float:
                if not np.isnan(e):
                    return True
            elif type(e) != int and type(e) != float:
                if e is not None:
                    return True

        except Exception as err:
            pass

        return False

    def isValueEmpty(self, e):
        return not self.isValNotEmpty(e)

    def getAsArray(self, name, index=None, type=float, keepPaddingNones=False, with_dates=False):

        full_data = self.get(name, index=index, keepPaddingNones=keepPaddingNones, with_dates=with_dates)

        # filter data and remove nans in the beginning
        if not with_dates:
            data = full_data
        else:
            data = full_data["data"]

        if data is not None and len(data) > 0:
            if self.isValueEmpty(data[0]):
                index = 0
                for f in data:
                    if self.isValueEmpty(f):
                        index = index + 1
                    else:
                        break
                data = data[index:]
        float_data = np.array(data, dtype=float)

        if with_dates:
            full_data["data"] = float_data
            return full_data

        return float_data

    ## This method combines all params and combine as a dataframe
    def df(self):
        return self.df

    def columns(self):
        return self.table.columns

    def getColumns(self):
        return self.table.columns

    def last(self, name, maxDistance=100, filterNone=False, replaceNone=None) -> LastEntry:

        data = None
        try:
            maybe_col_name = name
            if ":" in maybe_col_name:
                maybe_col_name = maybe_col_name.split(":")[0]

            # if its a key of inputs - lets export the right column
            if maybe_col_name in self.inputs:
                if isinstance(self.inputs[maybe_col_name], str):
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]))
                if self.inputs[maybe_col_name]["type"] == "dataInput":
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]["value"]))

            data = None
            if maybe_col_name + ":y" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":y")
            elif name in self.table.columns:
                data = self.table.getLastEntry(name, maxLength=maxDistance)
            elif "additionalData." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("additionalData." + maybe_col_name, maxLength=maxDistance)
            elif maybe_col_name + ":close" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":close", maxLength=maxDistance)
            elif "stats." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("stats." + maybe_col_name, maxLength=maxDistance)
            elif "stats." + name in self.table.columns:
                data = self.table.getLastEntry("stats." + name, maxLength=maxDistance)

        except Exception as e:
            self.logger().error(e)

        if data is not None:
            return data

        return data

    def getNow_date(self, index=-1):
        # when index is not integer
        if not isinstance(index, int) and not isinstance(index, np.int64):
            return index
        dt = self.table.index[min(index, len(self.table.index) - 1)]
        return dt

    def current(self, name):
        return self.get(name, index=-1)

    def statistic(self, name="r_master"):

        return self.current("stats."+name)

    def lastStatistic(self, name="r_master"):

        return self.last("stats."+name)

    def setVar(self, name, data, logicId=None):

        return self.var(name, data, logicId=logicId)

    def setUniqueName(self, name):
        self.uniqueName = name
        return name

    def getUniqueName(self):
        return self.uniqueName

    def price(self, chart="chart1"):
        return self.table.getLast(chart+".main:close")

    def isNaN(self, num):
        return num != num

    def additional(self, name):

        index = -1

        if "additionalData." + name in self.table.columns:
            data = self.table.lastElement("additionalData." + name)
            if self.isNaN(data):
                return None
            return data

        return None

    def date(self, index=-1):
        #date = pd.to_datetime(self.table.index[index]).to_pydatetime()
        date = self.table.index[index]
        return date

    def closeDate(self):
        #if len(self.table.index) > 0:
        #    date = pd.to_datetime(self.table.index[-1]).to_pydatetime()
        date = self.table.index[-1]
        return date

    def time(self):
        if len(self.table.index) > 0:
            date = pd.to_datetime(self.table.index[-1], infer_datetime_format=True)
            return date
        return None


    def varInfo(self, name, logicId=None):
        d = self.getLastData(logicId+".var."+name)
        return d

    ## This method adds a signal
    def var(self, name, data=None, logicId=None):

        if data is not None:
            return self._storageManager.setVar(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getVar(logicId if logicId is not None else self.getUniqueName(), name)

    def destroy(self):

        pass