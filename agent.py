from collections import deque
from statistics import fmean, pstdev

class TradingAgent:
    """Own intelligent agent: a mean-reversion trader with internal state.

        The market regime (uptrend / downtrend / sideway) is hidden, so the agent estimates
        the "normal" price from a rolling window of recent prices. When the price falls well
        below that mean (the demand zone), it buys. It sells only with a minimal profit margin.

        Internal state (memory):
            _window          - the last `windowLen` observed prices
            _averageBuyPrice - average price of the units currently held
            _lastBuyPrice    - price of the last buy; the next buy must be cheaper (averaging down)
            _lastSellPrice   - price of the last sell; the next sell must be higher (scaling out)
        """

    def __init__(self, windowLen, k = 1, minMargin = 0.03):
        """windowLen - number of past prices used to estimate the mean and volatility
        k - how many standard deviations below the mean counts as "cheap"
        minMargin - minimal relative profit (0.03 = 3 %) required to sell
        """
        self._window = deque(maxlen = windowLen)
        self._k = k
        self._minMargin = minMargin
        self._averageBuyPrice = 0
        self._lastBuyPrice = 0
        self._lastSellPrice = 0

    def makeDecision(self, perception):
        """Choose "buy", "sell" or "hold" from the current percept and the internal state."""
        budget = perception["budget"]
        holdings = perception["holdings"]
        ath, atl = perception["ath"], perception["atl"]
        price = perception["price"]


        self._window.append(price)

        # no open position = forget the reference prices of the previous one
        if holdings == 0:
            self._averageBuyPrice = 0
            self._lastBuyPrice = 0
            self._lastSellPrice = 0


        # not enough history yet to estimate mean and volatility reliably
        if len(self._window) < self._window.maxlen:
            return "hold"

        mu = fmean(self._window) #estimates normal price
        sigma = pstdev(self._window) #estimates volatility
        inDemandZone = (sigma > 0 and price < mu - self._k * sigma) #checks if the price is in the demand zone


        # averaging down: each further buy must be at least minMargin cheaper than the last one
        # (or a new all-time low, or the first buy of a position)
        isBetterPriceToBuy = (price < self._lastBuyPrice * (1 - self._minMargin) or price <= atl or self._lastBuyPrice == 0)

        # scaling out: each further sell must be at least minMargin higher than the last one
        # (or a new all-time high, or the first sell)
        isBetterPriceToSell = (price > self._lastSellPrice * (1 + self._minMargin) or price >= ath or self._lastSellPrice == 0)


        if inDemandZone and isBetterPriceToBuy and budget >= price:
            # update the average cost of the position including the new unit
            self._averageBuyPrice = (holdings * self._averageBuyPrice + price) / (holdings +1)
            self._lastBuyPrice = price
            # the first sell must already be profitable
            self._lastSellPrice = self._averageBuyPrice * (1 + self._minMargin)
            return "buy"

        # sell only with profit of at least minMargin over the average buy price
        if holdings > 0 and price > self._averageBuyPrice * (1 + self._minMargin) and isBetterPriceToSell:
            self._lastSellPrice = price
            return "sell"

        return "hold"





