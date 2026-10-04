from agent import TradingAgent
from environment import TradingMarket
from actuator import Actuator
from resultVizualization import plot_trading_session
from agent2 import BaseAgent
from sensor import Sensor
from operator import itemgetter

def runExp(agent,configWeights, configName, tradingConfigs, ticks=8000):
    startingPrice, ath, atl, minimalRegimeDuration, maximumRegimeDuration, initialBudget, seed = itemgetter("startingPrice",
                                                                                                      "ath",
                                                                                                      "atl",
                                                                                                      "minimalRegimeDuration",
                                                                                                      "maximumRegimeDuration",
                                                                                                      "initialBudget", "seed")(tradingConfigs)
    env = TradingMarket(seed, startingPrice, ath, atl, configWeights, minimalRegimeDuration, maximumRegimeDuration, initialBudget)
    sensor = Sensor(env)
    actuator = Actuator(env)

    for _ in range(ticks):
        env.tick()
        perception = sensor.sense()
        action = agent.makeDecision(perception)
        actuator.act(action)

    profit = env.getPortfolio() - env.getInitialBudget()
    plot_trading_session(env.getHistory(), env.tradeLog(), env.getPortfolio(), env.getInitialBudget(), configName)
    return profit


def runExpTradingAgent(configWeights, configName, windowLen, tradingConfigs):
    return runExp(TradingAgent(windowLen=windowLen,k=0.5),configWeights, configName, tradingConfigs)

def runExpBaseAgent(configWeights, configName, tradingConfigs):
    return runExp(BaseAgent(),configWeights, configName, tradingConfigs)


