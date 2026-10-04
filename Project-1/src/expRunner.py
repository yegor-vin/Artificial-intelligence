from agent import TradingAgent
from environment import TradingMarket
from actuator import Actuator
from resultVizualization import plot_trading_session
from agent2 import BaseAgent
from sensor import Sensor
from operator import itemgetter
from resultLogger import logRun, saveTradeLog
import time

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

    startTime = time.perf_counter()
    for _ in range(ticks):
        env.tick()
        perception = sensor.sense()
        action = agent.makeDecision(perception)
        actuator.act(action)

    seconds = time.perf_counter() - startTime
    profit = env.getPortfolio() - env.getInitialBudget()

    final = sensor.sense()             
    trades = env.tradeLog()
    logRun({
        "config": configName,
        "agent": type(agent).__name__,
        "seed": seed,
        "ticks": ticks,
        "seconds": round(seconds, 4),
        "profit": round(profit, 2),
        "finalPortfolio": round(env.getPortfolio(), 2),
        "cashAtEnd": round(final["budget"], 2),
        "holdingsAtEnd": final["holdings"],
        "buys": sum(1 for _, a, _ in trades if a == "buy"),
        "sells": sum(1 for _, a, _ in trades if a == "sell"),
    })
    saveTradeLog(trades, configName)

    plot_trading_session(env.getHistory(), env.tradeLog(), env.getPortfolio(), env.getInitialBudget(), configName)
    return profit


def runExpTradingAgent(configWeights, configName, windowLen, tradingConfigs):
    return runExp(TradingAgent(windowLen=windowLen,k=0.5),configWeights, configName, tradingConfigs)

def runExpBaseAgent(configWeights, configName, tradingConfigs):
    return runExp(BaseAgent(),configWeights, configName, tradingConfigs)


