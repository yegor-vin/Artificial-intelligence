from priceSimulator import PriceSimulator

class TradingMarket:
    def __init__(self, seed,  startingPrice, ath, atl, weights, minimalRegimeDuration, maximumRegimeDuration, initialBudget):

        if  not isinstance(startingPrice, int or float):
            raise ValueError("Price should be an integer or float")

        if startingPrice > ath:
            self._ath = startingPrice
            self._atl = atl
        elif startingPrice < atl:
            self._atl = startingPrice
            self._ath = ath
        else:
            self._ath = ath
            self._atl = atl

        self._priceSimulator = PriceSimulator(seed, startingPrice, weights, minimalRegimeDuration, maximumRegimeDuration)
        startPrice = self._priceSimulator.currentPrice
        self._currentPrice = startPrice
        self._history = [startPrice]
        self._budget = initialBudget

        self._holdings = 0
        self._ticksCounter = 0
        self._initialBudget = initialBudget
        self._tradeLog = []



    def tick(self):
        newPrice = self._priceSimulator.step()
        self._currentPrice = newPrice
        self._ath = max(newPrice, self._ath)
        self._atl = min(newPrice, self._atl)
        self._history.append(newPrice)
        self._ticksCounter += 1

    def getPerception(self):
        return {
            "price": self._currentPrice,
            "ath": self._ath,
            "atl": self._atl,
            "budget": self._budget,
            "holdings": self._holdings


        }

    def applyAction(self, action):

        if action == "buy" and self._budget >= self._currentPrice:
            self._holdings += 1
            self._budget -= self._currentPrice
            self._tradeLog.append((self._ticksCounter, action, self._currentPrice))
            return 1

        elif action == "sell" and self._holdings > 0:
            self._holdings -= 1
            self._budget += self._currentPrice
            self._tradeLog.append((self._ticksCounter, action, self._currentPrice))
            return -1

        return 0

    def isBunkrupt(self):
        return self._budget <=  0 and self._holdings == 0

    def displayPortfolio(self):
        return self._budget + self._holdings * self._currentPrice

    def tradeLog(self):
        return self._tradeLog

    def getHistory(self):
        return self._history

    def getInitialBduget(self):
        return self._initialBudget

    def getHoldings(self):
        return self._holdings



