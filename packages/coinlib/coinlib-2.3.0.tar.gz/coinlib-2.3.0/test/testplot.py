import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc

import numpy as np
import urllib
import datetime as dt

import mplfinance as mpf

import coinlib as c
from coinlib import LogicJob

import matplotlib.pyplot as plt
import numpy as np

c.connectAsDataAnalytics()

workspace = c.CoinlibWorkspace("642990f18ace5393cc941271", dataSetId="lGiYXXLR5dvYV92JGjHk",
                               chipmkunkdb_host="localhost")

def bytespdate2num(fmt, encoding='utf-8'):
    #strconverter = mdates.datestr2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return mdates.datestr2num(s)

    return bytesconverter

df = workspace.getDataFrame()

fig = plt.figure()
ax1 = plt.subplot2grid((1 ,1), (0 ,0))

"""
# Unfortunately, Yahoo's API is no longer available
# feel free to adapt the code to another source, or use this drop-in replacement.
stock_price_url = 'https://pythonprogramming.net/yahoo_finance_replacement'
source_code = urllib.request.urlopen(stock_price_url).read().decode()
stock_data = []
split_source = source_code.split('\n')
for line in split_source[1:]:
    split_line = line.split(',')
    if len(split_line) == 7:
        if 'values' not in line and 'labels' not in line:
            stock_data.append(line)


date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data,
                                                                  delimiter=',',
                                                                  unpack=True,
                                                                  converters={0: bytespdate2num('%Y-%m-%d')})

x = 0
y = 10
ohlc = []

while x < y:
    append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
    ohlc.append(append_me)
    x+=1
    """
chartData = "chart1"
ohlc = df.head(50)[['datetime', chartData+".main:open", chartData+".main:high",
                   chartData+".main:low", chartData+".main:close", chartData+".main:volume"]].copy()
ohlc["open"] = ohlc[chartData+".main:open"]
ohlc["close"] = ohlc[chartData+".main:close"]
ohlc["high"] = ohlc[chartData+".main:high"]
ohlc["low"] = ohlc[chartData+".main:low"]
ohlc["volume"] = ohlc[chartData+".main:volume"]

## clear nan values
ohlc = ohlc.dropna()

fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(20, 10))

mpf.plot(ohlc, block=True, type='line', ax=ax[0,0], axtitle='AAPL', xrotation=0)
print("ASD")