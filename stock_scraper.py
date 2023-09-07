import pandas as pd
import requests
import pickle
import matplotlib.pyplot as plt
import numpy as np

#will be doing trading on 2 year span, so clear trends can be established

def getTickers():
    df = pd.read_csv('SP500.csv')
    return df["Symbol"].tolist()

def scrapePrices(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    period1 = "1631000000" #approximately 2 years ago
    period2 = "1694105820" #end of sept 5th, 2023 (for testing purposes)

    querystring = {"period1": period1, "period2": period2, "interval": "60m", "includePrePost": "true",
                   "events": "div|split|earn", "lang": "en-US", "region": "US"}
    headers = {"User-Agent": "Insomnia/2023.5.7"}

    resp = requests.request("GET", url, headers=headers, params=querystring)
    data = resp.json()
    df = None
    try:
        df = pd.DataFrame.from_dict(data["chart"]["result"][0]["indicators"]["quote"][0])
        df = df[df["volume"] != 0]
        df.reset_index(drop=True, inplace=True)
        # print("df", df.tail())
    except:
        pass

    return df

def storeDataFrame():
    print("Num Tickers:", len(getTickers()))
    dfMap = {}
    cnt = 0
    for sym in getTickers():
        symDF = scrapePrices(sym)
        if symDF is not None and not symDF.empty:
            dfMap[sym] = symDF
        if cnt % 20 == 0:
            print(cnt)
        cnt += 1

    print("DF Map Len", len(dfMap))
    # save priceMap dict to stock_prices.pkl file
    with open('stock_prices.pkl', 'wb') as fp:
        pickle.dump(dfMap, fp)
        print('historical prices successfully stored')

def loadDataFrame():
    # Read dictionary pkl file
    dfMap = {}
    with open('stock_prices.pkl', 'rb') as fp:
        dfMap = pickle.load(fp)
        print('historical prices successfully loaded')

    return dfMap

def plotStockPrices(prices):
    x = np.array([i for i in range(1, len(prices) + 1)])
    y = np.array(prices)
    plt.plot(x, y)
    plt.show()