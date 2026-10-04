from expRunner import runExpTradingAgent
from expRunner import runExpBaseAgent

def prepareConfigs(conf1, conf2, conf3, conf4):
    confArray = [conf1,conf2,conf3,conf4]
    return confArray

def runExperiments(configs):
    tradingProfit = 0
    baseProfit = 0
    for i in range(4):
        tradingProfit += runExpTradingAgent(configs[i], f"config{i}-trading-agent-session")
        baseProfit += runExpBaseAgent(configs[i], f"config{i}-base-agent-session")
    tradingAverageProfit = tradingProfit / 4
    baseAverageProfit = baseProfit / 4

    print(tradingAverageProfit)
    print(baseAverageProfit)

runExperiments(prepareConfigs({"uptrend": 1, "downtrend": 1, "sideway": 1}, {"uptrend": 1, "downtrend": 1, "sideway": 3}, {"uptrend": 2, "downtrend": 1, "sideway": 3}, {"uptrend": 3, "downtrend": 1, "sideway": 1}))