from expRunner import runExp

def prepareConfigs(conf1, conf2, conf3, conf4):
    confArray = [conf1,conf2,conf3,conf4]
    return confArray

def runExperiments(configs):
    for i in range(4):
        runExp(configs[i])

runExperiments(prepareConfigs({"uptrend": 1, "downtrend": 1, "sideway": 1}, {"uptrend": 1, "downtrend": 1, "sideway": 3}, {"uptrend": 2, "downtrend": 1, "sideway": 3}, {"uptrend": 3, "downtrend": 1, "sideway": 1}))