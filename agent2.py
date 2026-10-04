class BaseAgent:
    """Baseline reflex agent: buys after a price drop, sells after a price rise.
      Remembers only the previous price, with no notion of trend, volatility or profit."""
    def __init__(self):
        self._previousPrice = 0

    def makeDecision(self, preception):
        badget = preception["budget"]
        price= preception["price"]
        holdings = preception["holdings"]

        if self._previousPrice == 0:
            self._previousPrice = price

        if self._previousPrice > price and badget >= price:
            action = "buy"

        elif self._previousPrice < price and holdings > 0:
            action = "sell"

        else:
            action = "hold"

        self._previousPrice = price
        return action

