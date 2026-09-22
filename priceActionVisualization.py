import matplotlib.pyplot as plt
from price_simulator import PriceSimulator

def simulate_path(seed, sim_config, n_ticks=500):
    sim = PriceSimulator(seed=seed, **sim_config)
    prices = [sim.currentPrice]
    regimes = [sim.currentRegime]
    for _ in range(n_ticks):
        prices.append(sim.step())
        regimes.append(sim.currentRegime)
    return prices, regimes


# --- Check 1: reproducibility (same seed = same path) ---
p1, _ = simulate_path(seed=42, sim_config={"startingPrice": 100})
p2, _ = simulate_path(seed=42, sim_config={"startingPrice": 100})
assert p1 == p2, "Reproducibility broken: same seed gave different paths"
print("Reproducibility check passed.")

# --- Check 2: never negative ---
p3, _ = simulate_path(seed=7, sim_config={"startingPrice": 100}, n_ticks=5000)
assert all(p > 0 for p in p3), "Price went non-positive"
print("Non-negativity check passed.")

# --- Check 3: visual inspection — different seeds ---
plt.figure(figsize=(10, 5))
for seed in [1, 2, 3]:
    prices, _ = simulate_path(seed=seed, sim_config={"startingPrice": 100})
    plt.plot(prices, label=f"seed={seed}")
plt.title("Different seeds -> different paths")
plt.xlabel("tick"); plt.ylabel("price"); plt.legend()
plt.savefig("check_seeds.png")

# --- Check 4: visual inspection — different configs ---
configs = {
    "ranging":  {"regimeWeight": {"sideway": 6, "uptrend": 1, "downtrend": 1}},
    "volatile": {"regimeWeight": {"sideway": 1, "uptrend": 1, "downtrend": 1},
                 "minimalRegimeDuration": 20, "maximalRegimeDuration": 60},
    "trending": {"regimeWeight": {"uptrend": 5, "sideway": 1, "downtrend": 1}},
}

fig, axes = plt.subplots(len(configs), 1, figsize=(10, 10), sharex=True)
for ax, (name, cfg) in zip(axes, configs.items()):
    prices, _ = simulate_path(seed=99, sim_config={"startingPrice": 100, **cfg})
    ax.plot(prices)
    ax.set_title(name)
plt.tight_layout()
plt.savefig("check_configs.png")

# --- Check 5: visual inspection — regime boundaries ---
prices, regimes = simulate_path(seed=6, sim_config={"startingPrice": 100})
plt.figure(figsize=(10, 5))
colors = {"uptrend": "green", "downtrend": "red", "sideway": "gray"}
for i in range(1, len(prices)):
    plt.plot([i-1, i], [prices[i-1], prices[i]], color=colors[regimes[i]])
plt.title("Price colored by regime")
plt.savefig("check_regimes.png")
