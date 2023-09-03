import pandas as pd
import requests
import pickle

#will be doing long term (not short term) trades (and will look for good time to buy and sell for each stock)
#essentially perform the overall trading operations on each stock and report net gain as a percent
# - and take average of all of the percents to see overall percent gain and compare to smp500 gain over past 10 years

def getTickers():
    df = pd.read_csv('SP500.csv')
    return df["Symbol"].tolist()

def scrapePrices(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    # period1 = "1535843336" #approximately 5 years ago
    period1 = "1378077047" #approximately 10 years ago
    period2 = "16936096250" #if you use a number much larger it will go up to current day

    # 5 year period, 1 day intervals
    querystring = {"": "", "events": "capitalGain|div|split", "formatted": "true", "includeAdjustedClose": "true",
                   "interval": "1d", "symbol": ticker, "userYfid": "true", "period1": period1,
                   "period2": period2, "lang": "en-US", "region": "US"}
    headers = {"User-Agent": "Insomnia/2023.5.7"}

    resp = requests.request("GET", url, headers=headers, params=querystring)
    data = resp.json()
    prices = None
    try:
        prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    except:
        pass

    return prices

def storePrices():
    print(len(getTickers()))
    priceMap = {}
    cnt = 0
    for sym in getTickers():
        symPrices = scrapePrices(sym)
        if symPrices is not None:
            priceMap[sym] = symPrices
        if cnt % 20 == 0:
            print(cnt)
        cnt += 1

    # save priceMap dict to stock_prices.pkl file
    with open('stock_prices.pkl', 'wb') as fp:
        pickle.dump(priceMap, fp)
        print('historical prices successfully stored')

def loadPrices():
    # Read dictionary pkl file
    priceMap = {}
    with open('stock_prices.pkl', 'rb') as fp:
        priceMap = pickle.load(fp)

    return priceMap
