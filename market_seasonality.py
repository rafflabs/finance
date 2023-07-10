import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use("seaborn-v0_8")
import seaborn

# Market Seasonality Analysis

Assets = [["iShares Core MSCI World UCITS ETF USD (Acc)","SWDA.MI"],
          ["iShares Core DAX UCITS ETF (DE)","EXS1.MI"]]

names = list(np.array(Assets)[:, 0])
tickers = list(np.array(Assets)[:, 1])

data = yf.download(tickers)["Adj Close"]
data = data.reindex(tickers, axis=1)

def season(data, year, n):
    year1 = year - n
    year2 = year - 1
    year1 = str(year1) + '-01-01'
    year2 = str(year2) + '-12-31'
    # print(year1, year2)
    sdata = data.loc[year1:year2].pct_change()
    sdata.reset_index(inplace=True)
    sdata['Date'] = sdata['Date'].apply(lambda x: x.replace(year=2020))
    sdata = sdata.resample('D', on='Date').mean()
    sdata = sdata + 1
    sdata[0:1] = 100
    sdata = sdata.cumprod()
    # print(sdata[sdata.isna().any(axis=1)])
    sdata.dropna(inplace=True)
    return sdata

seas_05 = season(data, 2023, 5)
seas_07 = season(data, 2023, 7)
seas_10 = season(data, 2023, 10)
seas_15 = season(data, 2023, 15)
seas_20 = season(data, 2023, 20)

seas_05['EXS1.MI'].plot(figsize=(25,15))
seas_07['EXS1.MI'].plot(figsize=(25,15))
seas_10['EXS1.MI'].plot(figsize=(25,15))
seas_15['EXS1.MI'].plot(figsize=(25,15))
seas_20['EXS1.MI'].plot(figsize=(25,15))
