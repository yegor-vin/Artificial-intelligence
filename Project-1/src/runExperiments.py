from expRunner import runExpTradingAgent
from expRunner import runExpBaseAgent
from compareAgentsVisualization import compareProfits
import json
from operator import itemgetter
from resultLogger import startLog

def prepareConfigs(conf1, conf2, conf3, conf4):
    confArray = [conf1,conf2,conf3,conf4]
    return confArray

def runExperiments(configs, tradingConfigs):
  startLog()
  minDuration, maxDuration = itemgetter(
  "minimalRegimeDuration",
  "maximumRegimeDuration")(tradingConfigs)

  windowLen = int((maxDuration + minDuration) * 0.5)

  tradingProfitArr = []
  baseProfitArr = []
  for i in range(4):
      tradingProfitArr.append(runExpTradingAgent(configs[i], f"config{i}-trading-agent", windowLen, tradingConfigs))
      baseProfitArr.append(runExpBaseAgent(configs[i], f"config{i}-base-agent", tradingConfigs))
  compareProfits(tradingProfitArr, baseProfitArr)


if __name__ == "__main__":
    # runs only when started directly: python src/runExperiments.py
    with open("tradingConfigs.json") as f:
        tradingConfigs = json.load(f)

    configs = prepareConfigs(
        {"uptrend": 1, "downtrend": 1, "sideway": 1},
        {"uptrend": 1, "downtrend": 1, "sideway": 3},
        {"uptrend": 2, "downtrend": 1, "sideway": 3},
        {"uptrend": 4, "downtrend": 1, "sideway": 1},
    )
    runExperiments(configs, tradingConfigs)