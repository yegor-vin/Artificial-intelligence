from expRunner import runExpTradingAgent
from expRunner import runExpBaseAgent
from compareAgentsVisualization import compareProfits
import json
from operator import itemgetter

with open("tradingConfigs.json") as f:
    tradingConfigs = json.load(f)

def prepareConfigs(conf1, conf2, conf3, conf4):
    confArray = [conf1,conf2,conf3,conf4]
    return confArray

def runExperiments(configs, tradingConfigs):
  minDuration, maxDuration = itemgetter(
  "minimalRegimeDuration",
  "maximumRegimeDuration")(tradingConfigs)

  windowLen = int((minDuration + maxDuration) * 0.5)

  tradingProfitArr = []
  baseProfitArr = []
  for i in range(4):
      tradingProfitArr.append(runExpTradingAgent(configs[i], f"config{i}-trading-agent-session", windowLen, tradingConfigs))
      baseProfitArr.append(runExpBaseAgent(configs[i], f"config{i}-base-agent-session", tradingConfigs))
  compareProfits(tradingProfitArr, baseProfitArr)

runExperiments(prepareConfigs({"uptrend": 1, "downtrend": 1, "sideway": 1}, {"uptrend": 1, "downtrend": 1, "sideway": 3}, {"uptrend": 2, "downtrend": 1, "sideway": 3}, {"uptrend": 4, "downtrend": 1, "sideway": 1}), tradingConfigs)