import random

class PriceSimulator:
    regimes = {
        "uptrend": {"mu": 0.006, "sigma": 0.01},
        "downtrend": {"mu": 0.006, "sigma": 0.01},
        "sideway": {"mu": 0, "sigma": 0.006}
    }

    def __init__(self, seed, startingPrice, regimeWeight = None, minimalRegimeDuration = 50, maximalRegimeDuration = 200,):
        if startingPrice <= 0:
            raise ValueError("starting price must be positive")
        if minimalRegimeDuration <= 0 or maximalRegimeDuration < minimalRegimeDuration:
            raise ValueError("invalid regime duration bounds")

        self._randomNumberGenerator = random.Random(seed);
        self._dt = 1.0
        self._minimalRegimeDuration = minimalRegimeDuration
        self._maximalRegimeDuration = maximalRegimeDuration
        self._regimesWeights =regimeWeight or  {
            "uptrend": 1, "downtrend": 1, "sideway": 1,
        }

        self._validateWeights()
        self.currentPrice = startingPrice
        self._tickCounter = 0

        self._regime = None
        self.ticksLeft = 0
        self._changeRegime()

    def _validateWeights(self):
        unknown = set(self._regimesWeights) - set(self.regimes)
        if unknown:
            raise ValueError(f"unknown regime in weights: {unknown}")
        if all(w <= for w in self._regimesWEights.values()):
    def _changeRegime(self):


