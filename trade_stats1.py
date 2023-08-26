#!/usr/bin/python3


import csv


takeProfit = 10
takeLoss = 10


tradeSuccess = 0
tradeFail = 0
tradeCount = 0

candle_list = {}

def BuyTrade(idx):
    candleTrade = candle_list[idx]
    buyPrice = candleTrade['close']
    for v in range(idx - 1, 0, -1):
        candle = candle_list[v]
        if candle['min'] <= (buyPrice - takeLoss):
            print("Trade: {}, candles: {},  Entry: {}, Loss: {}".format(
                candleTrade['date'], idx - v, buyPrice, candle['min']))
            return False

        if candle['max'] >= (buyPrice + takeProfit):
            print("Trade: {}, candles: {},  Entry: {}, Gain: {}".format(
                candleTrade['date'], idx - v, buyPrice, candle['max']))
            return True

    # Unfinished trade, fail.
    return False

with open('trade_stats1.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, dialect='excel')
    i = 0
    for row in datareader:
        if i == 0:
            i += 1
            continue

        c_date = row[0]
        c_open = float(row[1].replace(',', '.'))
        c_max = float(row[2].replace(',', '.'))
        c_min = float(row[3].replace(',', '.'))
        c_close = float(row[4].replace(',', '.')) 
        c_signal =float(row[5].replace(',', '.')) 
        candle_list[i - 1] = { 'date': c_date, 'open': c_open, 
                              'max': c_max, 'min': c_min, 'close': 
                              c_close, 'signal': c_signal }
        i += 1

for t in range(i - 2, 0, -1):
    candle = candle_list[t]
    if candle['signal'] == 1:
        tradeCount += 1
        if BuyTrade(t):
            tradeSuccess += 1 
        else:
            tradeFail += 1 

if tradeCount > 0:
    print("tradeSuccess: {},  {:.2f}%".format(tradeSuccess, tradeSuccess/tradeCount * 100))
    print("tradeFail: {},  {:.2f}%".format(tradeFail, tradeFail/tradeCount * 100))
    print("Trades: {}".format(tradeCount))
