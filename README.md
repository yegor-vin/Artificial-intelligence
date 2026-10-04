# Trading Agent – Intelligent Agent Assignment

A simulated single-asset market in which an autonomous **trading agent** buys and sells
to maximize profit. Its results are compared with a simple **base (reflex) agent**
on the same market, with the same seed and settings.

## Requirements

- Python 3.10 or newer (developed with Python 3.14)
- External library: `matplotlib` (used only for charts)
- Standard library modules used: `random`, `math`, `json`, `statistics`, `collections`, `operator`

## Installation

```bash
# optional: create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # or: pip install matplotlib
```

## Running

Run the program from the project folder:

```bash
python runExperiments.py
```

The program runs both agents on 4 market configurations. For each configuration,
it saves a price chart with buy/sell markers and a final comparison chart (see [Output](#output)).

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
  "seed": 34
}
```

| Key | Meaning |
|---|---|
| `startingPrice` | price of the asset at tick 0 (also the long-term mean the price reverts to) |
| `ath` / `atl` | initial all-time high / all-time low the agent knows in advance |
| `minimalRegimeDuration` / `maximumRegimeDuration` | how long one hidden market regime lasts (in ticks) |
| `initialBudget` | the agent's starting cash |
| `seed` | random seed; the same seed always produces the same market, so every run is reproducible |

### Market configurations – `runExperiments.py`

Each configuration sets how often each hidden regime is chosen (`uptrend`, `downtrend`, `sideway`):

| Name | Weights (up : down : sideway) |
|---|---|
| config0 | 1 : 1 : 1 – balanced |
| config1 | 1 : 1 : 3 – mostly sideways |
| config2 | 2 : 1 : 3 – mild uptrend |
| config3 | 4 : 1 : 1 – strong uptrend |

To change them, edit the arguments of `prepareConfigs(...)` on the last line of `runExperiments.py`.

### Other parameters

| Parameter | Where | Default |
|---|---|---|
| session length (ticks) | `ticks` in `runExp`, `expRunner.py` | 8000 |
| trading agent `k` (std-devs below the mean to buy) | `runExpTradingAgent`, `expRunner.py` | 0.5 |
| trading agent `minMargin` (minimal profit to sell) | `TradingAgent.__init__`, `agent.py` | 0.03 |
| trading agent `windowLen` | computed in `runExperiments.py` | (min + max regime duration) / 2 |

## Output

All files are saved in the project folder:

| File | Content |
|---|---|
| `config{i}-trading-agent-session.png` | price chart of the trading agent's session with buy (▲) and sell (▼) markers, initial and final portfolio, profit |
| `config{i}-base-agent-session.png` | the same for the base agent |
| `Comparison.png` | mean profit of both agents with standard deviation |

**Profit** = final portfolio − initial budget. Units still held at the end are valued
at the last market price.

## Project structure

| File | Role |
|---|---|
| `priceSimulator.py` | generates prices: geometric Brownian motion with hidden regimes and mean reversion |
| `environment.py` | `TradingMarket` – the environment; holds the true state (price, ATH/ATL, budget, holdings, trade log) and applies actions |
| `sensor.py` | `Sensor` – the agent's only way to observe the environment (price, ATH, ATL, budget, holdings) |
| `actuator.py` | `Actuator` – carries out the agent's action (`buy`, `sell`, `hold`) in the environment |
| `agent.py` | `TradingAgent` – own agent: buys when the price falls below `mean − k·std` of a rolling window, sells only with at least `minMargin` profit |
| `agent2.py` | `BaseAgent` – reflex agent: buys after a price drop, sells after a price rise |
| `expRunner.py` | runs one session: sense → decide → act loop for a fixed number of ticks, returns profit |
| `runExperiments.py` | entry point; loads the configuration, runs all experiments, draws the comparison |
| `resultVizualization.py` | price chart of one session |
| `compareAgentsVisualization.py` | comparison chart of both agents |

## How one session works

```
for each tick:
    environment.tick()                  # new price is generated
    percept = sensor.sense()            # agent observes price, ATH, ATL, budget, holdings
    action  = agent.makeDecision(percept)
    actuator.act(action)                # environment executes buy / sell / hold
```

The agent never accesses the environment directly. It sees only the percept, and the
current market regime stays hidden from it.

## Reproducing a run

Set `seed` in `tradingConfigs.json` and run `python runExperiments.py`. The same seed
and settings always produce the same prices, trades and profits.
