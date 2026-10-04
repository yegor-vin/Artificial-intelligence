from expRunner import runExpTradingAgent
from expRunner import runExpBaseAgent
from compareAgentsVisualization import compareProfits

def prepareConfigs(conf1, conf2, conf3, conf4):
    confArray = [conf1,conf2,conf3,conf4]
    return confArray

def runExperiments(configs):
    tradingProfitArr = []
    baseProfitArr = []
    for i in range(4):
        tradingProfitArr.append(runExpTradingAgent(configs[i], f"config{i}-trading-agent-session"))
        baseProfitArr.append(runExpBaseAgent(configs[i], f"config{i}-base-agent-session"))

    compareProfits(tradingProfitArr, baseProfitArr)

runExperiments(prepareConfigs({"uptrend": 1, "downtrend": 1, "sideway": 1}, {"uptrend": 1, "downtrend": 1, "sideway": 3}, {"uptrend": 2, "downtrend": 1, "sideway": 3}, {"uptrend": 3, "downtrend": 1, "sideway": 1}))