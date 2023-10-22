import abc
import asyncio
import json
import threading
import time
from abc import ABC ,abstractmethod
from enum import Enum
import uuid
import base64
from typing import List
import datetime

import aio_pika
import sys
import asyncio
import pytz
import requests
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from chipmunkdb.ChipmunkDb import ChipmunkDb
from coinlib import helper

from coinlib.Registrar import Registrar

import pandas as pd

from coinlib.feature.FeatureDTO import ProcessResponse, FeatureInfos, FeatureDatabaseInfo, RabbitInfo


class FeatureWorkerInterface:
    def send_event(self, name, data):
        pass
    def getIdentifier(self):
        pass


class CoinlibFeature(ABC):
    def __init__(self):
        self.saveTimer = None
        self.options = None
        self.fetcher_info = None
        self.databaseInfo = None
        self.worker : FeatureWorkerInterface = None
        self.session_data  = {}
        self._stopped = False
        self.rabbit_info : RabbitInfo = None
        self.loop = None
        self.saveloop = asyncio.new_event_loop()
        self.timer_list = {}
        self.registrar = Registrar()
        self.timers = {}
        self.defaultInterval = 60 * 1000
        self.transactions = {
            "default": {
                "data": [],
                "interval": self.defaultInterval,
                "datetime": None
            }
        }

        pass

    def isLiveEnvironment(self):
        return self.registrar.isLiveEnvironment()

    def alarm(self, *params):

        message = ""
        for param in params:
            message += str(param) + "\r\n "
        try:
            data_server_target = self.databaseInfo.server

            backend = self.registrar.coinlib_backend_host
            if backend is None:
                backend = "http://" + self.registrar.workerEndpoint + ":9001"
            if backend is None:
                backend = 'http://localhost:9001'
            url = backend + "/api/v1/historicalfeatures/alarm/" + data_server_target

            data = requests.post(url,
                                 json={
                                     "feature": self.databaseInfo.id,
                                     "message": message
                                 },
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'text/plain'})

            if data.status_code == 200:
                return data.json()

        except Exception as e:
            print("Can not send alarm to " + data_server_target + " " + self.databaseInfo.id + " " + str(e))
            pass
        return None

    def logger(self):
        return self.registrar.logger

    def set_worker(self, worker):
        self.worker = worker

    @staticmethod
    def formatInterval(dt, interval: int):
        offset_time = 0
        utcoffset = dt.utcoffset()
        if utcoffset is not None:
            offset_time = utcoffset.microseconds
        # timestamp for "zero"
        timestamp = int(dt.timestamp() * 1000)

        # build new timestamp
        newtime = int(timestamp / interval) * interval
        newdt = datetime.datetime.fromtimestamp(newtime / 1000, dt.tzinfo)

        return newdt

    def transaction(self, interval=60 * 60 * 1000):
        newid = uuid.uuid4()
        self.transactions[newid] = {
            "data": [],
            "interval": interval,
            "datetime": CoinlibFeature.formatInterval(datetime.datetime.now(pytz.utc), interval)
        }
        return newid

    def triggerRun(self, params):
        return False

    def is_data_open(self):
        if self.transactions["default"]["data"] is not None and len(self.transactions["default"]["data"]) > 0:
            return True
        return False

    def saveDataAfterWriteTimeout(self):
        self.saveTimer.cancel()

        return self.saveloop.run_until_complete(self.save_data_transaction("default"))

    def session(self, parameter=None, value=None):
        sess = self.session_data
        if parameter is not None:
            if value is not None:
                self.session_data[parameter] = value
                self.save_session_data()
                return value
            if parameter in sess:
                return sess[parameter]
            else:
                return None
        if value is not None:
            self.save_session_data()
            self.session_data = value
            return value
        return sess

    def save_statistics(self, features, count):
        if self.worker is not None:
            self.worker.send_event("save_statistics", {"features": features, "count": count})
            return True
        return True

    def save_session_data(self):
        if self.worker is not None:
            self.worker.send_event("save_session", self.session_data)
            return True
        return False

    async def save_data_transaction(self, transactionid):
        data = self.transactions[transactionid]["data"]

        stage = "_dev"
        if self.registrar.isLiveEnvironment():
            stage = ""

        latest_data_with_symbol = {}
        df = pd.DataFrame()
        columns = []
        rows = {}
        for row in data:
            datetime_as_str = datetime.datetime.strftime(row["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
            fullindex = datetime_as_str

            orig_key = row["identifier"]
            key = orig_key+stage
            full_identifier = row["identifier"]+stage
            if row["group"] is not None:
                full_identifier = row["group"]+"."+full_identifier
                key = row["group"]+"."+key
            full_key = key
            if row["symbol"] is not None:
                fullindex = fullindex + "_" + row["symbol"]
                full_key = full_key + "_" + row["symbol"]
            if row["exchange"] is not None:
                fullindex = fullindex + "_" + row["exchange"]
                full_key = full_key + ":" + row["exchange"]

            d = {}

            if key not in columns:
                columns.append({
                    "id": key,
                    "key": orig_key,
                    "datetime": datetime_as_str,
                    "value": row["value"],
                    "group": row["group"],
                    "stage": "dev" if self.registrar.isLiveEnvironment() else "live"
                })
            if fullindex not in rows:
                rows[fullindex] = {}
            latest_data_with_symbol[full_key] = {
                "value": row["value"],
                "identifier": full_identifier,
                "group": row["group"],
                "symbol": row["symbol"],
                "exchange": row["exchange"],
                "id": full_key,
                "datetime": row["datetime"]
            }
            rows[fullindex]["datetime"] = row["datetime"]
            rows[fullindex]["symbol"] = row["symbol"]
            rows[fullindex]["index"] = fullindex
            rows[fullindex][key] = row["value"]

        list = []
        for key in rows:
            list.append(rows[key])

        df = pd.DataFrame(list)
        df2 = df.set_index("index")

        return await self.save_dataframe(df2, columns, self.databaseInfo.server, self.databaseInfo.id)

    async def save_dataframe(self, df2, columns, databaseServer: str, databaseId: str):
        try:
            try:
                data_server_target = databaseServer

                data = df2.to_csv()
                message_body = json.dumps({
                    "keys": columns, "data": data,
                    "transaction_id": 123,
                    "source": self.worker.getIdentifier() if self.worker else None
                },
                    default=helper.serializeDTO)

                backend = self.registrar.coinlib_backend_host
                if backend is None:
                    backend = "http://"+self.registrar.workerEndpoint+":9001"
                if backend is None:
                    backend = 'http://localhost:9001'
                url = backend+"/api/v1/historicalfeatures/save/"+data_server_target

                requests.post(url, data=message_body, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

            except Exception as e:
                print("Can not save data to "+databaseServer+" "+databaseId+" "+str(e))
                pass

            self.save_statistics(columns, df2.shape[0])
        except Exception as e:
            print(e)
        return True



    def get_data_range(self, identifier=None):
        try:
            data_server_target = self.databaseInfo.server

            backend = self.registrar.coinlib_backend_host
            if backend is None:
                backend = "http://" + self.registrar.workerEndpoint + ":9001"
            if backend is None:
                backend = 'http://localhost:9001'
            url = backend + "/api/v1/historicalfeatures/range/" + data_server_target

            data = requests.post(url,
                                 json={
                                        "id": identifier,
                                        "stage": "dev" if not self.registrar.isLiveEnvironment() else "live"
                                       },
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'text/plain'})

            if data.status_code == 200:
                return data.json()

        except Exception as e:
            print("Can not read data from " + data_server_target + " " + self.databaseInfo.id + " " + str(e))
            pass
        return None

    def get_data(self, identifier=None, start=None, end=None, query=None, limit=-1):
        try:
            data_server_target = self.databaseInfo.server

            backend = self.registrar.coinlib_backend_host
            if backend is None:
                backend = "http://" + self.registrar.workerEndpoint + ":9001"
            if backend is None:
                backend = 'http://localhost:9001'
            url = backend + "/api/v1/historicalfeatures/read/" + data_server_target

            if query is None:
                query = {
                        "datetime": {
                            "$gte": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            "$lte": end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                    }

                }

            data = requests.post(url,
                                 json={
                                        "id": identifier,
                                        "query": query,
                                         "limit": limit,
                                        "stage": "dev" if not self.registrar.isLiveEnvironment() else "live"
                                       },
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'text/plain'})

            if data.status_code == 200:
                return data.json()

        except Exception as e:
            print("Can not read data from " + data_server_target + " " + self.databaseInfo.id + " " + str(e))
            pass
        return None

    def delete_data(self, identifier=None, group=None):
        try:

            chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(self.databaseInfo.server))
            if identifier is not None:
                id = identifier

                chipmunkDb.dropColumn(self.databaseInfo.id, id, domain=group)
            else:
                chipmunkDb.dropCollection(self.databaseInfo.id)

        except Exception as e:
            raise e
        return None

    def clear_transaction(self, transaction):
        if transaction != "default" and transaction in self.transactions:
            del self.transactions[transaction]
        elif transaction == "default":
            self.transactions["default"] = {
                "data": [],
                "interval": self.defaultInterval,
                "datetime": None
            }


    def write_data(self, identifier, value, symbol=None, exchange=None, interval=None,
                   dt=None, group=None, transaction=None, additonalData=None):

        if transaction is None:

            if interval is None:
                self.transactions["default"]["interval"] = self.defaultInterval
                interval = self.defaultInterval

            if dt is None and self.transactions["default"]["datetime"] is None:
                dt = CoinlibFeature.formatInterval(datetime.datetime.now(pytz.utc), interval)
                self.transactions["default"]["datetime"] = dt
            elif dt is None:
                dt = self.transactions["default"]["datetime"]
            else:
                dt = CoinlibFeature.formatInterval(dt, interval)



            row = {
                "identifier": identifier,
                "value": value,
                "symbol": symbol,
                "exchange": exchange,
                "datetime": dt,
                "group": group
            }
            if additonalData is not None:
                row.update(additonalData)
            self.transactions["default"]["data"].append(row)

            # start a timer interval to write data when x seconds are gone
            if self.saveTimer is not None:
                self.saveTimer.cancel()
                self.saveTimer = None
            self.saveTimer = threading.Timer(2.0, self.saveDataAfterWriteTimeout)
            self.saveTimer.start()
        else:

            if interval is None:
                interval = self.transactions[transaction]["interval"]

            if dt is None:
                dt = self.transactions[transaction]["datetime"]
            else:
                dt = CoinlibFeature.formatInterval(dt, interval)
            row = {
                    "identifier": identifier,
                    "value": value,
                    "symbol": symbol,
                    "exchange": exchange,
                    "datetime": dt,
                    "group": group
                }
            if additonalData is not None:
                row.update(additonalData)
            if transaction in self.transactions:
                self.transactions[transaction]["data"].append()
            else:
                self.logger().error("Transactionn does not exist")
                return False

        return True

    def finish_transaction_sync(self, transaction_id):

        self.saveloop.run_until_complete(self.save_data_transaction(transaction_id))

        return True

    async def finish_transaction(self, transaction_id):

        await self.save_data_transaction(transaction_id)

        return True

    def cancelAllTimer(self):
        for name in self.timer_list:
            self.cancel_timer(name)

    def stop(self):
        self._stopped = True
        self.cancelAllTimer()

    def isRunning(self):
        return not self._stopped

    def isStopped(self):
        return self._stopped

    def cancel_timer(self, name: str):
        if name in self.timer_list:
            self.timer_list[name].cancel()
            return True
        return False

    def timer_was_called(self, interval, name, process):
        if self._stopped:
            return True
        if name in self.timer_list:
            self.timer_list[name] = threading.Timer(interval, self.timer_was_called, args=[ interval, name, process])
            self.timer_list[name].start()
            try:
                self.saveloop.run_until_complete(process())
            except Exception as e:
                print(e)


    def timer(self, timeintervalsec: int, name: str, process, firstStartDirect=True):

        self.timer_list[name] = "idle"
        if firstStartDirect:
            self.timer_list[name] = threading.Timer(1.0, self.timer_was_called, args=[ timeintervalsec, name, process])
        else:
            self.timer_list[name] = threading.Timer(timeintervalsec, self.timer_was_called,
                                                    args=[ timeintervalsec, name, process])
        self.timer_list[name].start()
        return True

    def register_timer(self, timeinterval, name: str, process, firstStartDirect=True):
        return self.timer(timeinterval, name, process,firstStartDirect=firstStartDirect)

    def option(self, name):
        return self.getOption(name)

    def options(self):
        return self.getOptions()

    def get_option(self, name):
        return self.getOption(name)

    def getOption(self, name):
        try:
            if self.options is not None:
                return self.options[name]
        except Exception as e:
            print("Error ", str(e))
            pass

        return None

    def getOptions(self):
        return self.options

    async def start_run_process(self):
        pass

    def set_rabbit_info(self, rabbit: RabbitInfo):
        self.rabbit_info = rabbit

    def set_session_id(self, id):
        self.session_id = id

    def set_session_data(self, session_data):
        self.session_data = session_data

    def set_database_info(self, databaseInfo: FeatureDatabaseInfo):
        self.databaseInfo = databaseInfo

    def before_start(self):

        pass

    async def start(self, loop, options):
        self.loop = loop
        self.options = options

        self.before_start()

        return await self.start_run_process()

    @abstractmethod
    async def get_feature_infos(self) -> List[FeatureInfos]:
        return []
