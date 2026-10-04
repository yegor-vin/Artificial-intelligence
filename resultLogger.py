import csv
import os

RESULTS_DIR = "results"
RUNS_FILE = os.path.join(RESULTS_DIR, "runs.csv")
RUN_COLUMNS = ["config", "agent", "seed", "ticks", "seconds", "profit",
               "finalPortfolio", "cashAtEnd", "holdingsAtEnd", "buys", "sells"]


def startLog():
    os.makedirs(os.path.join(RESULTS_DIR, "trades"), exist_ok=True)
    with open(RUNS_FILE, "w", newline="") as f:
        csv.writer(f).writerow(RUN_COLUMNS)


def logRun(row):
    with open(RUNS_FILE, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=RUN_COLUMNS).writerow(row)


def saveTradeLog(tradeLog, configName):
    path = os.path.join(RESULTS_DIR, "trades", f"{configName}.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tick", "action", "price"])
        writer.writerows(tradeLog)