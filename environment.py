

class tradingMarket:
    def __init__(self, currentPrice, ath, atl):
        self._currentPrice = currentPrice

        if currentPrice > ath:
            self._ath = currentPrice
        elif currentPrice < atl:
            self._atl = currentPrice
        else:
            self._ath = ath
            self._atl = atl

    def update(self, newPrice):
        self._currentPrice = newPrice
        self._ath = max(newPrice, self._ath)
        self._atl = min(newPrice, self._atl)

    def getPerception(self):
        return 