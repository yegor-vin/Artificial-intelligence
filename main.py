import resultVizualization
from agent import TradingAgent
from environment import TradingMarket
from actuator import Actuator
from resultVizualization import plot_trading_session
def main():
    a = TradingAgent(k=0.5)
    env = TradingMarket(18, 270, 574, 165, {"uptrend": 1, "downtrend": 1, "sideway": 1}, 50, 150, 1000)
    actuator = Actuator(env)
    for _ in range(12500):
        env.tick()
        perception = env.getPerception()
        action = a.makeDecision(perception)
        actuator.act(action)

        if env.isBunkrupt():
            break

    # while not env._holdings == 0:
    #     env.tick()
    #     perception = env.getPerception()
    #     action = a.makeDecision(perception)
    #     actuator.act(action)
    print(a._lastBuyPrice)


    return plot_trading_session(env.getHistory(), env.tradeLog(), env.displayPortfolio(), env.getInitialBduget(), env.getHoldings())



main()
