from agent import TradingAgent
from environment import TradingMarket

def main():
    a = TradingAgent(windowLen=3, k=0.5)
    for p in [100, 100, 100]:
        a.makeDecision({"price": p, "budget": 1000, "holdings": 0, "ath": 200, "atl": 50})
    print(a.makeDecision({"price": 90, "budget": 1000, "holdings": 0, "ath": 200, "atl": 50}))

main()
