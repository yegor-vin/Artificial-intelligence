import matplotlib.pyplot as plt

def plot_trading_session(price_history, trade_log, final_portfolio, initial_budget, title):
    """
    price_history: list of prices, one per tick (index = tick number)
    trade_log: list of (tick, action, price) tuples, e.g. from env.trade_log()
    """
    ticks = range(len(price_history))

    plt.figure(figsize=(14, 6))
    plt.plot(ticks, price_history, color="steelblue", linewidth=1, label="Price", zorder=1)

    buy_ticks = [t for t, action, price in trade_log if action == "buy"]
    buy_prices = [price for t, action, price in trade_log if action == "buy"]

    sell_ticks = [t for t, action, price in trade_log if action == "sell"]
    sell_prices = [price for t, action, price in trade_log if action == "sell"]

    plt.scatter(buy_ticks, buy_prices, color="green", marker="^", s=50,
                label="Buy", zorder=3)
    plt.scatter(sell_ticks, sell_prices, color="red", marker="v", s=50,
                label="Sell", zorder=3)

    plt.title(f"{title} — Portfolio: initial {initial_budget:.2f}, final {final_portfolio:.2f}, profit {final_portfolio - initial_budget:.2f}")
    plt.xlabel("Tick")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_')}.png")
    plt.close()