from agent import TradingAgent
from environment import TradingMarket
from actuator import Actuator
from resultVizualization import plot_trading_session
def runExp(configWeights):
    a = TradingAgent(k=0.5)
    env = TradingMarket(43, 120, 574, 64, {"uptrend": 2, "downtrend": 1, "sideway": 3}, 50, 150, 1000)
    actuator = Actuator(env)
    for _ in range(7000):
        env.tick()
        perception = env.getPerception()
        action = a.makeDecision(perception)
        actuator.act(action)

        if env.isBunkrupt():
            break

    while not env._holdings == 0:
        env.tick()
        perception = env.getPerception()
        action = a.makeDecision(perception)
        actuator.act(action)



    return plot_trading_session(env.getHistory(), env.tradeLog(), env.displayPortfolio(), env.getInitialBduget(), env.getHoldings())




