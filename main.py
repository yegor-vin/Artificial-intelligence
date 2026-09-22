from agent import TradingAgent
from environment import TradingMarket

def TradingSession():
    environment = TradingMarket(9, 200, 500, 150, {"uptrend" : 1, "downtrend" : 1, "sideway": 1}, 100, 500)
    agent = TradingAgent(1000,)
    while True:
