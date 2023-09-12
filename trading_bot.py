import numpy as np
import pandas_ta as ta
import pickle

def updateDFWithEMA(dfMap):
    for sym in dfMap.keys():
        dfMap[sym]["emaShort"] = ta.ema(dfMap[sym]["close"], length=40)
        dfMap[sym]["emaMid"] = ta.ema(dfMap[sym]["close"], length=70)
        dfMap[sym]["emaLong"] = ta.ema(dfMap[sym]["close"], length=100)

        backrollingN = 5
        dfMap[sym]["slopeEMAShort"] = dfMap[sym]["emaShort"].diff(periods=1)
        dfMap[sym]["slopeEMAShort"] = dfMap[sym]["slopeEMAShort"].rolling(window=backrollingN).mean()

        dfMap[sym]["slopeEMAMid"] = dfMap[sym]["emaMid"].diff(periods=1)
        dfMap[sym]["slopeEMAMid"] = dfMap[sym]["slopeEMAMid"].rolling(window=backrollingN).mean()

        dfMap[sym]["slopeEMALong"] = dfMap[sym]["emaLong"].diff(periods=1)
        dfMap[sym]["slopeEMALong"] = dfMap[sym]["slopeEMALong"].rolling(window=backrollingN).mean()

        #find signal
        conditions = [(dfMap[sym]["emaShort"] < dfMap[sym]["emaMid"]) & (dfMap[sym]["emaMid"] < dfMap[sym]["emaLong"]) & (dfMap[sym]["slopeEMAShort"] < 0) & (dfMap[sym]["slopeEMAMid"] < 0) & (dfMap[sym]["slopeEMALong"] < 0),
                      (dfMap[sym]["emaShort"] > dfMap[sym]["emaMid"]) & (dfMap[sym]["emaMid"] > dfMap[sym]["emaLong"]) & (dfMap[sym]["slopeEMAShort"] > 0) & (dfMap[sym]["slopeEMAMid"] > 0) & (dfMap[sym]["slopeEMALong"] > 0)]
        choices = [1,2] #1 is down trend, 2 is up trend, 0 is inconclusive
        dfMap[sym]["emaSignal"] = np.select(conditions, choices, default = 0)

        totalSig = [0 for _ in range(len(dfMap[sym]))]

        for i in range(len(dfMap[sym])):
            if dfMap[sym]["emaSignal"][i] == 1 and dfMap[sym]["open"][i] > dfMap[sym]["emaShort"][i] > dfMap[sym]["close"][i]:
                totalSig[i] = 1 #sell
            elif dfMap[sym]["emaSignal"][i] == 2 and dfMap[sym]["open"][i] < dfMap[sym]["emaShort"][i] < dfMap[sym]["close"][i]:
                totalSig[i] = 2 #buy

        dfMap[sym]["totalSignal"] = totalSig

    with open('stock_prices.pkl', 'wb') as fp:
        pickle.dump(dfMap, fp)
        print('dataframe successfully updated')
