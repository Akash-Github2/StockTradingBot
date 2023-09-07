import stock_scraper as scraper
import trading_bot as bot
import math

#trading on 2 year span, so clear trends can be established
def backtest(dfMap):
    avgPosStockPriceNetGain = 0
    avgPosObtainedNetGain = 0 #when positive price change
    posCount = 0
    avgNegStockPriceNetGain = 0
    avgNegObtainedNetGain = 0 #when negative price change
    negCount = 0
    for ticker in dfMap.keys():
        print(ticker)
        df = dfMap[ticker]
        totalBuyAmount = 0
        totalSellAmount = 0
        numShares = 0

        simpDF = df[df["totalSignal"] > 0] #only need to look at buy/sell positions
        simpDF.reset_index(drop=True, inplace=True)

        for i in range(len(simpDF)):
            if simpDF["totalSignal"][i] == 1: #sell
                if numShares > 0:
                    totalSellAmount += simpDF["close"][i]
                    numShares -= 1
            elif simpDF["totalSignal"][i] == 2: #buy
                totalBuyAmount += simpDF["close"][i]
                numShares += 1
            else:
                print("ERROR")

        lastPrice = df["close"][len(df)-1]

        totalSellAmount += numShares * lastPrice
        numShares = 0
        netGainPercent = (totalSellAmount / totalBuyAmount - 1) * 100 #percent we grew
        priceNetGainPercent = (lastPrice / df["close"][0] - 1) * 100 #percent the price went up

        if math.isnan(totalBuyAmount) or math.isnan(totalSellAmount) or math.isnan(netGainPercent) or math.isnan(priceNetGainPercent):
            totalBuyAmount = totalSellAmount = netGainPercent = priceNetGainPercent = 0
        print(str(round(netGainPercent, 4)) + "%", str(round(priceNetGainPercent, 4)) + "%")
        if priceNetGainPercent >= 0:
            avgPosObtainedNetGain += netGainPercent
            avgPosStockPriceNetGain += priceNetGainPercent
            posCount += 1
        else:
            avgNegObtainedNetGain += netGainPercent
            avgNegStockPriceNetGain += priceNetGainPercent
            negCount += 1
    if posCount > 0:
        avgPosObtainedNetGain /= posCount
        avgPosStockPriceNetGain /= posCount
    if negCount > 0:
        avgNegObtainedNetGain /= negCount
        avgNegStockPriceNetGain /= negCount

    print("Final:", str(round(avgPosObtainedNetGain, 4)) + "%", str(round(avgPosStockPriceNetGain, 4)) + "%", str(round(avgNegObtainedNetGain, 4)) + "%", str(round(avgNegStockPriceNetGain, 4)) + "%")

def main():
    scraper.storeDataFrame()
    dfMap = scraper.loadDataFrame()
    bot.updateDFWithEMA(dfMap)
    dfMap = scraper.loadDataFrame()
    # print(dfMap["GOOGL"].tail())
    # print(dfMap["GOOGL"]["totalSignal"].value_counts())
    backtest(dfMap)

if __name__ == '__main__':
    main()
