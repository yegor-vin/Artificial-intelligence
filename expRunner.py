from agent import TradingAgent
from environment import TradingMarket
from actuator import Actuator
from resultVizualization import plot_trading_session
from agent2 import BaseAgent

def runExpTradingAgent(configWeights, configName):
    a = TradingAgent(k=0.5)
    env = TradingMarket(43, 120, 574, 64, configWeights, 50, 150, 1000)
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


    profit = env.getPortfolio() - env.getInitialBudget()
    plot_trading_session(env.getHistory(), env.tradeLog(), env.getPortfolio(), env.getInitialBudget(), configName)
    return profit

def runExpBaseAgent(configWeights, configName):
    a = BaseAgent()
    env = TradingMarket(43, 120, 574, 64, configWeights, 50, 150, 1000)
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
    profit = env.getPortfolio() - env.getInitialBudget()
    plot_trading_session(env.getHistory(), env.tradeLog(), env.getPortfolio(), env.getInitialBudget(), configName)
    return profit





