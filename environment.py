from price_simulator import PriceSimulator

class TradingMarket:
    def __init__(self, seed,  startingPrice, ath, atl, weights, minimalRegimeDuration, maximumRegimeDuration, agent):

        if  not isinstance(startingPrice, int or float):
            raise ValueError("Price should be an integer or float")

        if startingPrice > ath:
            self._ath = startingPrice
        elif startingPrice < atl:
            self._atl = startingPrice
        else:
            self._ath = ath
            self._atl = atl

        self._priceSimulator = PriceSimulator(seed, startingPrice, weights, minimalRegimeDuration, maximumRegimeDuration)
        startPrice = self._priceSimulator.currentPrice
        self._history = [startPrice]


        self._priceSimulator = PriceSimulator(seed, startingPrice, weights, minimalRegimeDuration, maximumRegimeDuration)
        self._agent = agent

    def update(self, newPrice):
        self._currentPrice = newPrice
        self._ath = max(newPrice, self._ath)
        self._atl = min(newPrice, self._atl)

    def sendPerception(self):

    def sendInitialMarketState(self):
        self._agent.sensor()
