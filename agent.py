class TradingAgent:

    def __init__(self, budget ):
        if budget <= 0:
            raise ValueError("budget must be positive")

        self._budget = budget

    # def makeDecision(self, currentPrice):
    #
    # def act(self, currentPrice):
