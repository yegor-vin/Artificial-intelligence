# Trading Agent – Intelligent Agent Assignment

A simulated single-asset market in which an autonomous **trading agent** buys and sells
to maximize profit. Its results are compared with a simple **base (reflex) agent**
on the same market, with the same seed and the same settings.

## Requirements

- Python 3.10 or newer (developed with Python 3.14)
- External library: `matplotlib` (used only for charts)
- Standard library modules used: `random`, `math`, `json`, `csv`, `os`, `time`,
  `statistics`, `collections`, `operator`

The agents' decision logic uses no external library.

## Installation

```bash
cd Project-1

# optional: create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Running

**Always start the program from the project root** (the folder that contains
`tradingConfigs.json`). All file paths are relative to this folder.

```bash
cd Project-1
python src/runExperiments.py
```

In PyCharm, set *Run → Edit Configurations… → Working directory* to the `Project-1` folder
(not `src/`).

The program runs both agents on 4 market configurations (8 sessions in total) and saves
the results to `results/` (see [Output](#output)). It prints nothing to the console.

## Project structure

```
Project-1/
├── README.md
├── requirements.txt
├── tradingConfigs.json          market settings and seed
├── src/
│   ├── runExperiments.py        entry point
│   ├── expRunner.py             runs one session (sense → decide → act)
│   ├── environment.py           TradingMarket – the environment
│   ├── priceSimulator.py        price generator with hidden regimes
│   ├── sensor.py                Sensor – what the agent can observe
│   ├── actuator.py              Actuator – executes the agent's action
│   ├── agent.py                 TradingAgent – own intelligent agent
│   ├── agent2.py                BaseAgent – baseline reflex agent
│   ├── resultLogger.py          writes runs.csv and trade logs
│   ├── resultVizualization.py   price chart of one session
│   └── compareAgentsVisualization.py   comparison chart
└── results/
    ├── runs.csv
    ├── trades/
    └── graphics/
```

| File | Role |
|---|---|
| `priceSimulator.py` | generates prices as geometric Brownian motion; drift and volatility depend on a hidden regime (uptrend / downtrend / sideway); a weak mean-reversion term pulls the price toward the starting price |
| `environment.py` | `TradingMarket` holds the true state (price, ATH/ATL, budget, holdings, trade log) and applies actions; impossible actions (buy without money, sell without holdings) are ignored |
| `sensor.py` | `Sensor` is the agent's only way to observe the market: price, ATH, ATL, budget, holdings. The regime stays hidden. |
| `actuator.py` | `Actuator` carries out the chosen action (`buy`, `sell`, `hold`) |
| `agent.py` | `TradingAgent` buys when the price falls below `mean − k·std` of a rolling price window (demand zone) and sells only with at least `minMargin` profit |
| `agent2.py` | `BaseAgent` buys after any price drop and sells after any price rise |
| `expRunner.py` | runs one session for a fixed number of ticks, computes the profit, logs the run and draws its chart |
| `runExperiments.py` | loads the settings, runs every agent on every configuration, draws the comparison |

## How one session works

```
for each tick (8000 ticks):
    environment.tick()                    # a new price is generated
    percept = sensor.sense()              # agent observes price, ATH, ATL, budget, holdings
    action  = agent.makeDecision(percept) # "buy", "sell" or "hold"
    actuator.act(action)                  # environment executes the action
```

The agent never accesses the environment directly. It sees only the percept.

**Performance measure:** profit = final portfolio − initial budget, where
final portfolio = cash + held units × last market price.

## Configuration

### Market settings – `tradingConfigs.json`

```json
{
  "startingPrice": 140,
  "ath": 573,
  "atl": 78,
  "minimalRegimeDuration": 50,
  "maximumRegimeDuration": 150,
  "initialBudget": 800,
  "seed": 44
}
```

| Key | Meaning |
|---|---|
| `startingPrice` | price at tick 0; also the long-term mean the price reverts to |
| `ath` / `atl` | initial all-time high / low that the agent knows in advance |
| `minimalRegimeDuration` / `maximumRegimeDuration` | how long one hidden regime lasts, in ticks |
| `initialBudget` | the agent's starting cash |
| `seed` | random seed; the same seed always produces the same market |

### Market configurations – `src/runExperiments.py`

Each configuration sets how often each hidden regime is drawn (weights `uptrend : downtrend : sideway`):

| Name | Weights | Market type |
|---|---|---|
| config0 | 1 : 1 : 1 | balanced |
| config1 | 1 : 1 : 3 | mostly sideways |
| config2 | 2 : 1 : 3 | mild uptrend |
| config3 | 4 : 1 : 1 | strong uptrend |

To change them, edit the dictionaries passed to `prepareConfigs(...)` in the
`if __name__ == "__main__":` block of `runExperiments.py`.

### Other parameters

| Parameter | Where | Value |
|---|---|---|
| session length (ticks) | `ticks` in `runExp`, `src/expRunner.py` | 8000 |
| trading agent `k` – standard deviations below the mean that count as "cheap" | `runExpTradingAgent`, `src/expRunner.py` | 0.5 |
| trading agent `minMargin` – minimal relative profit to sell | `TradingAgent.__init__`, `src/agent.py` | 0.03 (3 %) |
| trading agent `windowLen` – length of the price window | computed in `src/runExperiments.py` | (min + max regime duration) / 2 = 100 |

## Output

All results are written to `results/` and overwritten on every run.

| File | Content |
|---|---|
| `results/runs.csv` | one row per session: `config, agent, seed, ticks, seconds, profit, finalPortfolio, cashAtEnd, holdingsAtEnd, buys, sells` |
| `results/trades/config{i}-{agent}.csv` | full course of one session: every executed trade as `tick, action, price` |
| `results/graphics/config{i}-trading-agent.png` | price chart of the trading agent's session with buy (▲) and sell (▼) markers, initial and final portfolio, profit |
| `results/graphics/config{i}-base-agent.png` | the same for the base agent |
| `results/graphics/Comparison.png` | mean profit of both agents over all configurations, with standard deviation |

`{i}` is the configuration number 0–3, `{agent}` is `trading-agent` or `base-agent`.

## Reproducing a run

Set `seed` in `tradingConfigs.json` and run `python src/runExperiments.py` from the
project root. The same seed and settings always produce the same prices, trades and
profits. To test a different market, change only the seed.
