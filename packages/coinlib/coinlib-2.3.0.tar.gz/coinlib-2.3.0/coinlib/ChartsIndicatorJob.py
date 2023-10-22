import copy
import datetime

import datetime
import pytz
import pandas as pd
import numpy as np

from coinlib.helper import taBox
from coinlib.BasicJob import BasicJob
import time

from coinlib.data.DataTable import DataTable
import json

def isFullOHLC(row):
    return (row.close != 0 and row.close != None and row.open != 0 and row.open != None and
            row.high != 0 and row.high != None and row.low != None and row.low != 0)


def is_in_list(allboxes, box):
    for b in allboxes:
        if b.top == box.top and b.bottom == box.bottom and b.left == box.left and b.right == box.right:
            return True
    return False


class ChartsIndicatorJob(BasicJob):
    def __init__(self, name, group, inputs, df, indicator, worker):
        super(ChartsIndicatorJob, self).__init__(df if type(df) == DataTable else DataTable(df), inputs)
        self.name = name
        self.group = group
        self.send = False
        self.chunked = False
        self.worker = worker
        self.data = []
        self.indicator = indicator
    
    def isChunked(self):
        return self.chunked
    
    def setChunked(self, chunked):
        self.chunked = chunked
        return True

    def getUniqueName(self):
        return self.uniqeName

    def getDateTimeFromISO8601String(self, s):
        import datetime
        import dateutil.parser
        d = dateutil.parser.parse(s)
        return d

    def findIndicatorInElements(self, name, chartConfig):
        for ind in chartConfig.elements:
            if ind.indicator.name == name:
                return ind

        for ind in chartConfig.elements:
            if "." in name:
                parentname = name.split(".")[0]

                if ind.indicator.name == parentname:
                    return ind
        return None

    def indicatorForInput(self, inputName: str):

        inputConfig = self.inputs
        correct_name = None
        for inp_key in dict.keys(inputConfig):
            inp_data = inputConfig[inp_key]
            if inp_key == inputName:
                if inp_data["value"] is not None:
                    correct_name = inp_data["value"]["value"]
                    break

        if correct_name is None:
            return None



        chartConfig = self.worker.chartConfig
        indicator = self.findIndicatorInElements(correct_name, chartConfig)

        if indicator is not None:
            return indicator.indicator

        return None

    def rgb2hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def color(self, color, higher_lower):
        """
           Lightens the given color by multiplying (1-luminosity) by the given amount.
           Input can be matplotlib color string, hex string, or RGB tuple.

           Examples:
           >> lighten_color('g', 0.3)
           >> lighten_color('#F034A3', 0.6)
           >> lighten_color((.3,.55,.1), 0.5)
           """
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        rgbs = colorsys.hls_to_rgb(c[0], 1 - higher_lower * (1 - c[1]), c[2])

        rgbhex = self.rgb2hex(int(rgbs[0] * 255), int(rgbs[1] * 255), int(rgbs[2] * 255))
        return rgbhex

    def convertBoxes(self, boxesList: [[{"top": float, "bottom": float}]]):
        eboxes = self.emptyList(len(boxesList))

        for i in range(len(boxesList)):
            boxes = boxesList[i]
            if boxes is None:
                continue
            eboxes[i] = json.dumps(boxes)
        return eboxes

    def emptySeries(self, l=None, emptyData=np.nan):
        if l is None:
            l = self.table.length()
        d = np.empty(l)
        d[:] = emptyData
        return d

    def emptyList(self, l=None, emptyData=None):
        if l is None:
            l = self.table.length()
        d = []
        for i in range(l):
            d.append(emptyData)
        return d

    def fillBoxSequentialInList(self, data: list, box: taBox, paddingleft=0):
        for i in range(box.left+paddingleft, min(box.right+paddingleft+1, len(data))):

            if box.get_top() <= 0 or box.get_bottom() <= 0:
                continue

            if data[i] == np.nan or data[i] is None:
                data[i] = []

            # when the box does not exist in the list
            # by the same top and bottom values
            # then we add it to the list
            if len(data[i]) > 0:
                ignore = False
                for b in data[i]:
                    if b["top"] == box.top and b["bottom"] == box.bottom:
                        ignore = True
                if not ignore:
                    data[i].append(box.get_HLBox())
            else:
                data[i].append(box.get_HLBox())
        return data
    
    def series(self, chartType, name, data, color=None,
               opacity=None,
               chartTypeIcon=None,
               size=None, tooltip=True, chart=None,
               fill=None, fill_from=None,
               fill_to=None, connectGaps=False):
        """
        Create a visible data series. This is the "rendered" Data in the chart.

        @chartType:
                    cloud,
                    series,
                    horizontal, (data can be single float or int)
                    marker,
                    buyselltriggers,
                    line,
                    dotted, (then color must be a array)
                    hist (then color must be a array)
        @chart: In which chart should it be shown - default is the chart with Index 0 but maybe you want another
        @name: This is the name of your data series if you have multiples
        @color: This is the choosen color
        @opacity: This is the opacity of the chart data
        @chartTypeIcon: Only available for "marker" - you ca select the icon for the marker
        @size: The size of the marker
        @tooltip: The tooltip if needed - for example this is a text when mouse is over marker
        """
        if color is None:
            color = "#ccffcc"


        utc=pytz.UTC
        latestDate = datetime.datetime(1971, 3, 19, 13, 0, 9, 351812)
        latestDate = utc.localize(latestDate)
        additional = {}

        column_names = []
        # check if output data is a series, a dataframe or a array
        if isinstance(data, (list, pd.core.series.Series, pd.DataFrame, int, float, np.ndarray)):
            if chartType == "horizontal":
                additional["yValue"] = data
            elif chartType == "cloud":

                self.table.setColumn(":top", data["top"])
                self.table.setColumn(":middle", data["middle"])
                self.table.setColumn(":bottom", data["bottom"])
                column_names = [":top", ":middle", ":bottom"]
            elif chartType == "marker" or chartType == "cross":
                # it is a numpy array
                if isinstance(data, (pd.core.series.Series)):
                    self.table.setColumn(":marker", data.values, type=str)
                else:
                    self.table.setColumn(":marker", data, type=str)
                column_names = [":marker"]
            elif chartType == "boxes":
                listdata = self.emptyList()
                allboxes = []
                originCloseData = np.array(self.get("symbol"))
                padding_from_left = len(listdata) - len(data)
                if padding_from_left > len(listdata)/2:
                    padding_from_left = len(self.table.index) - len(originCloseData)

                # we want to iterate over all data and select the boxes
                # than we check and modify create small boxes for each index
                # when its not a box we just add None
                for i in range(len(data)):
                    if data[i] is not None:
                        if isinstance(data[i], list) or isinstance(data[i], np.ndarray):
                            for box in data[i]:
                                listdata = self.fillBoxSequentialInList(listdata, box, padding_from_left)
                                if not is_in_list(allboxes, box):
                                    allboxes.append(box)
                        else:
                            box = data[i]
                            allboxes.append(box)
                            listdata = self.fillBoxSequentialInList(listdata, data[i], padding_from_left)
                listdata = self.convertBoxes(listdata)
                self.table.setColumn(":boxes", listdata, type=str)

                """
                drawableList = self.emptyList()
                for b in allboxes:
                    if drawableList[b.left+padding_from_left] is None:
                        drawableList[b.left+padding_from_left] = []
                    drawableList[b.left+padding_from_left].append(b)

                drawableListJsoned = self.emptyList()
                for i in range(len(drawableList)):
                    dw = drawableList[i]
                    if dw is not None:
                        nlist = []
                        for b in dw:
                            if b.top == 0 or b.bottom == 0:
                                continue

                            # lets deepcopy the box
                            bc = copy.deepcopy(b)
                            bc.left = datetime.datetime.strftime(self.getNow_date(b.left+padding_from_left), "%Y-%m-%dT%H:%M:%S.%fZ")
                            bc.right = datetime.datetime.strftime(self.getNow_date(b.right+padding_from_left), "%Y-%m-%dT%H:%M:%S.%fZ")
                            nlist.append(bc)
                        drawableListJsoned[i] = json.dumps(nlist, default=lambda o: o.__dict__)

                self.table.setColumn(":boxes_drawables", drawableListJsoned, type=str)
                """
                column_names = [":boxes"]

            elif chartType == "trendline" or chartType == "rayline":
                # it is a numpy array
                if isinstance(data, (pd.core.series.Series)):
                    self.table.setColumn(":marker", data.values, type=str)
                else:
                    self.table.setColumn(":marker", data, type=str)

                column_names = [":marker"]

            elif isinstance(data, (list)):
                # its a list
                self.table.setColumn(":y", data)
                column_names = [":y"]

            elif isinstance(data, (int, float)):

                self.table.setColumn(":y", [data])
                column_names = [":y"]

            elif isinstance(data, (pd.core.series.Series)):

                self.table.setColumn(":y", data.values)
                column_names = [":y"]

            elif isinstance(data, (pd.DataFrame)):
                # its a dataframe
                self.table.setColumn(":open", data["open"])
                self.table.setColumn(":high", data["high"])
                self.table.setColumn(":low", data["low"])
                self.table.setColumn(":close", data["close"])
                self.table.setColumn(":volume",  data["volume"])
                column_names = [":open", ":high", ":low", ":close", ":volume"]

            elif isinstance(data, (np.ndarray)):
                # it is a numpy array
                self.table.setColumn(":y", data)
                column_names = [":y"]


        else:
            raise Exception("Please send your data as pandas.series, list, ndarray or pd.dataframe")

        ## special case for histogram
        if isinstance(color, (list)) or isinstance(color, (np.ndarray)):
            self.table.setColumn(":color", color)
            column_names.append(":color")
            color = ":color"

        options = {}

        if color is not None:
            options["color"] = color
        if opacity is not None:
            options["opacity"] = opacity
        if tooltip is not None:
            options["tooltip"] = tooltip
        if size is not None:
            options["size"] = size
        if fill is not None:
            options["fill"] = fill
        if fill_from is not None:
            options["fill_from"] = fill_from
        if fill_to is not None:
            options["fill_to"] = fill_to
        if chartType == "cross":
            options["chartTypeIcon"] = "\ue84a"
        if chartTypeIcon is not None:
            options["chartTypeIcon"] = chartTypeIcon

        options["additional"] = json.dumps(additional)
        options["connectGaps"] = connectGaps
        options["chartType"] = chartType
        options["chart"] = str(chart) if chart is not None else None
        """
        try:
            chart["data"] = df[column_names]
        except Exception as e:
            log.error(e)
            pass
        chart["options"] = options"""

        self.worker.onPartialChartDataReceived(self.indicator, name,
                                               self.table.subTable(columns=column_names),
                                               options)

        return True
    
    
    def line(self, chartType, name, selector, data):
        
        return True
    
    
    def plot(self, chartType, name, selector, data):
        
        return True
    
    def getSessionData(self):
        
        sess_list = None
        columns = []
        for colname in self.df.columns:
            if (colname.startswith("session:") and "Datetime" not in colname):
                columns.append(colname)
        
        if (len(columns) > 0):
            sessionDf = pd.DataFrame(self.df, columns=columns)

            sessionDf["date"] = sessionDf.index.to_series().apply(lambda x: x.isoformat())
            ###sessionDf.select_dtypes(exclude=['datetime', 'datetime64','datetimetz'])
            sessionDf.reset_index(drop=True, inplace=True)
            ##sessionDf.drop(columns='session:Datetime')

            sess_list = sessionDf.to_dict()
            
            

        return sess_list
