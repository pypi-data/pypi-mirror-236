import math
from datetime import datetime

import matplotlib
import pandas as pd
from chipmunkdb.ChipmunkDb import ChipmunkDb
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import matplotlib.ticker as mticker

from matplotlib.dates import date2num

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import simplejson as json

from coinlib.DataWorker import WorkerJobListener
from coinlib.config import grpc_chan_ops
from coinlib.helper import is_in_ipynb
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
from coinlib.Registrar import Registrar
import grpc

import inspect
from google.protobuf.json_format import MessageToDict
import os
import sys
from google.protobuf.json_format import MessageToJson

from coinlib.logics.LogicOfflineWorkerTrader import LogicOfflineWorkerTrader
from coinlib.logics.manager.PortfolioModel import PortfolioModel


class LogicOfflineWorkerTraderLocally(LogicOfflineWorkerTrader):

    def __init__(self, workspaceId, dataSetId, runnerLogic, onLogicDataFinished, factory):
        super().__init__( statsModel.WorkerJob(), factory)
        self.dataSetId = dataSetId
        self.runnerLogic = runnerLogic
        self.workspaceId = workspaceId
        self.onLogicDataFinished = onLogicDataFinished

    def getJobConfig(self):
        workspaceInfo = statsModel.WorkspaceInfo()
        workspaceInfo.workspaceId = self.workspaceId
        workspaceInfo.dataSetId = self.dataSetId
        workspaceInfo.activityId = "12345"
        return self.logicInterface.GetLogicConfigForWorkspace(workspaceInfo, metadata=self.registrar.getAuthMetadata())

    def broadcastCurrentPercentage(self, percentage, manager):
        print(str(percentage*100)+" %")

    def onFinishedProcess(self):
        self.stop()

    def onErrorProcess(self, e):
        self.stop()

    def onWorkerJobProcessStarted(self, thread):
        thread.join()

    def generateLogicComponentsInfo(self):

        class Object(object):
            enabled = True
            identifier = "logic"
            pass
        self.logicComponentsWithInfo = []

        s = Object()
        s.info = {
            "process": self.runnerLogic
        }
        s.logic = Object()
        s.details = {}
        self.logicComponentsWithInfo.append(s)


        return self.logicComponentsWithInfo

    def setDataFrame(self, df):
        self.df = df

    def onLogicRunningFinished(self):
        print("Finished")

        filter_col = [col for col in self.dataFrame if col.startswith('logics')]

        return self.onLogicDataFinished(filter_col, self)

class CoinlibWorkspace:
    channel = None
    dataWorker = None

    def __init__(self, workspaceId, dataSetId=None, mode="dev",  chipmkunkdb_host=None):
        self.registrar = Registrar()

        self.dataWorker = WorkerJobListener(simulator=True)
        self.dataWorker.start()

        self.workspaceId = workspaceId
        self.dataSetId = dataSetId
        self.mode = mode
        self.db = ChipmunkDb(chipmkunkdb_host, 8091, autoConnect=True)
        if self.dataSetId is None:
            self.printAvailableDatasets()
            raise Exception("Please select a dataset")

    def printDatasetInfo(self, datasetId):
        dataset = self.db.collection_info(datasetId)
        print("------------------")
        print(datasetId.split("_")[2])
        try:
            start_date = self.db.query("SELECT * FROM "+datasetId+" ORDER BY  datetime ASC LIMIT 1")
            print("Start: "+start_date[0]["datetime"])
            start_date = self.db.query("SELECT * FROM " + datasetId + " ORDER BY  datetime DESC LIMIT 1")
            print("End: " + start_date[0]["datetime"])
        except:
            pass
        print(dataset)
        print("------------------\r\n")



    def printAvailableDatasets(self):
        print("Please select a available dataset:")
        for dataset in self.db.collections():
            if self.workspaceId in dataset["name"] and len(dataset["name"].split("_")) < 4 and dataset["rows"] is not None and len(dataset["name"].split("_")) > 2:
                self.printDatasetInfo(dataset["name"])

    def getDataFrame(self, mode=None):
        if mode is None:
            mode = self.mode
        if self.dataSetId is None:
            self.printAvailableDatasets()
            return None
        else:
            df = self.db.collection_as_pandas(mode+"_"+self.workspaceId+"_"+self.dataSetId)

        return df

    def subplotGraph(self, fig, df, title, series, chartData):
        relevantData = ['datetime', chartData+".main:open", chartData+".main:high",
                   chartData+".main:low", chartData+".main:close", chartData+".main:volume"]
        for s in series:
            if ":" in s["data"]:
                col = s["data"]
            else:
                col = s["data"] + ":y"
            s["data"] = col
            if col in df.columns:
                relevantData.append(col)


        ohlc = df[relevantData].copy()
        ohlc["open"] = ohlc[chartData + ".main:open"]
        ohlc["close"] = ohlc[chartData + ".main:close"]
        ohlc["high"] = ohlc[chartData + ".main:high"]
        ohlc["low"] = ohlc[chartData + ".main:low"]
        ohlc["volume"] = ohlc[chartData + ".main:volume"]
        ## clear nan values
        ohlc = ohlc.dropna()

        plots = []
        for serie in series:
            plots.append( mpf.make_addplot(ohlc[serie["data"]], type='line', ax=fig))

        mpf.plot(ohlc, ax=fig, type='candle', addplot=plots, axtitle=title)


    def plotLargeDataGrid(self, all_signals, series=[], windows=1, chartData="chart1"):
        """
        This method generates n-windows of a matplotlib and plots all signals in a
        subplot of each window. It should help you to get a overview of all moments that happened.
        """

        for window in range(windows):
            fig, ax = plt.subplots(nrows=math.floor(len(all_signals)/windows/3)+1, ncols=3, figsize=(20, 10))
            index = 0
            for i, signal in enumerate(all_signals):
                if i < window * (math.floor(len(all_signals)/windows)):
                    continue
                if i >= (window + 1) * math.floor(len(all_signals)/windows):
                    break

                df = signal["df"]
                title = signal["title"]
                self.subplotGraph(ax[math.floor(index / 3), index % 3], df, title, series, chartData)
                index = index + 1

        plt.show(block=True)


    def getAllSignalsDataFrame(self, codeCallback, signals: [] = None, before_min=120, after_min=200):
        self.registrar.isRegistered = True
        loadedData = {}

        def onLogicDataFinished(filter_col, worker):
            global loadedData
            listOfSignalTimestamps = {}

            for s in filter_col:
                if "signal"  in s:

                    sname = "_".join(s.split(".")[2:])
                    if signals is not None:
                        if sname not in signals:
                            continue
                    listOfSignalTimestamps[sname] = []
                    data = worker.dataFrame.loc[worker.dataFrame[s].isnull() == False, s]
                    lastIndex = None
                    for index, row in data.iteritems():

                        if lastIndex is None or (index - lastIndex).total_seconds() > 60:
                            lastIndex = index

                            df = worker.dataFrame.loc[index - pd.Timedelta(minutes=before_min):index + pd.Timedelta(minutes=after_min)]
                            listOfSignalTimestamps[sname].append({
                                "datetime": index,
                                "signal": row,
                                "df": df,
                                "title": str(index)
                            })
                        lastIndex = index

            return listOfSignalTimestamps

        workerJobProcess = LogicOfflineWorkerTraderLocally(self.workspaceId, self.dataSetId,
                                                           codeCallback, onLogicDataFinished, self.dataWorker)

        loadedData = workerJobProcess.startProcess()

        return loadedData




