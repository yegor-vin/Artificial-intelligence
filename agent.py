from collections import deque
from statistics import fmean, pstdev

class TradingAgent:

    def __init__(self, windowLen = 50, k = 1, minMargin = 0.03):
        self._window = deque(maxlen = windowLen)
        self._k = k
        self._minMargin = minMargin
        self._averageBuyPrice = 0
        self._lastBuyPrice = 0
        self._lastSellPrice = 0

    def makeDecision(self, perception):
        budget = perception["budget"]
        holdings = perception["holdings"]
        ath, atl = perception["ath"], perception["atl"]
        price = perception["price"]


        self._window.append(price)

        if holdings == 0:
            self._averageBuyPrice = 0
            self._lastBuyPrice = 0
            self._lastSellPrice = 0

        if len(self._window) < self._window.maxlen:
            return "hold"


        mu = fmean(self._window)
        sigma = pstdev(self._window)
        inDemandZone = (sigma > 0 and price < mu - self._k * sigma)
        inSupplyZone = (sigma > 0 and price > mu + self._k * sigma)

        if inDemandZone:
            self._lastSellPrice = price


        isBetterPriceToBuy = (price < self._lastBuyPrice * (1 - self._minMargin) or price <= atl or self._lastBuyPrice == 0)
        isBetterPriceToSell = (price > self._lastSellPrice * (1 + self._minMargin) or price >= ath or self._lastSellPrice == 0)


        if inDemandZone and isBetterPriceToBuy and budget >= price and not inSupplyZone:
            self._averageBuyPrice = (holdings * self._averageBuyPrice + price) / (holdings +1)
            self._lastBuyPrice = price
            self._lastSellPrice = mu + self._k * sigma
            return "buy"



        elif holdings > 0 and price > self._averageBuyPrice * (1 + self._minMargin) and isBetterPriceToSell:
            self._lastSellPrice = price
            return "sell"

        return "hold"





