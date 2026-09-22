import random
import math

class PriceSimulator:
    regimes = {
        "uptrend": {"mu": 0.006, "sigma": 0.01},
        "downtrend": {"mu": -0.006, "sigma": 0.01},
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
        self._ticksLeft = 0
        self._changeRegime()

    def _validateWeights(self):
        unknown = set(self._regimesWeights) - set(self.regimes)
        if unknown:
            raise ValueError(f"unknown regime in weights: {unknown}")
        if all(w <= 0 for w in self._regimesWeights.values()):
            raise ValueError("At least one regime weight must be positive")


    def _changeRegime(self):
         regimes, weights = zip(*self._regimesWeights.items())
         self._regime = self._randomNumberGenerator.choices(regimes, weights=weights, k=1)[0]
         self._ticksLeft = self._randomNumberGenerator.randint(self._minimalRegimeDuration, self._maximalRegimeDuration)

    def step(self):

        if self._ticksLeft <= 0:
            self._changeRegime()
        self._ticksLeft -= 1

        params = self.regimes[self._regime]
        z = self._randomNumberGenerator.gauss(0, 1)

        # log-return update — price stays strictly positive by construction
        log_return = (
                (params["mu"] - 0.5 * params["sigma"] ** 2) * self._dt
                + params["sigma"] * math.sqrt(self._dt) * z
        )
        self.currentPrice *= math.exp(log_return)
        self.currentPrice = max(self.currentPrice, 0.01)

        self._tickCounter += 1
        return self.currentPrice

    @property
    def currentRegime(self):
        return self._regime

