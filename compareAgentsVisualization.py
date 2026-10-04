from statistics import fmean, stdev
import matplotlib.pyplot as plt

def compareProfits(tradingProfits, baseProfits):
    means = []
    means.append(fmean(tradingProfits))
    means.append(fmean(baseProfits))
    stds = []
    stds.append(stdev(tradingProfits))
    stds.append(stdev(baseProfits))

    plt.figure(figsize=(8, 5))
    plt.bar(["Trading agent", "Base agent"], means, yerr=stds, capsize=6, color=["#2a6fdb", "#d9741a"])
    plt.ylabel("Profit")
    plt.savefig("Comparison.png")
    plt.close()

