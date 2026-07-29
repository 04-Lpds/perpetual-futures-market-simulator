# visualization.py
"""
Visualizations for the Simulator
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_price_path_debug(price_history, oracle_prices, liquidation_volumes):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    steps = range(len(price_history))
    ax1.plot(steps, price_history, label="Mark Price", color='blue')

    # Fix length mismatch
    if len(oracle_prices) == len(price_history) - 1:
        oracle_prices = [price_history[0]] + oracle_prices  # align lengths

    ax1.plot(steps, oracle_prices, label="Oracle Price", color='orange', linestyle='--')

    ax1.set_title("Price Path (Debug)")
    ax1.legend()
    ax1.grid(True)

    # Liquidation volume
    vol_steps = range(len(liquidation_volumes))
    ax2.bar(vol_steps, liquidation_volumes, color='red', alpha=0.6)
    ax2.set_ylabel("Liquidation Volume")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


def plot_market_dashboard(state, oracle_prices, funding_history, liquidation_times, liquidation_volumes,
                          funding_interval=3600, dt=1.0):
    """Professional dark-themed dashboard"""
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np

    plt.style.use('dark_background')  # dark theme

    n = len(state.price_history)
    steps = np.arange(n)
    time_hours = steps * dt / 3600.0

    fig = plt.figure(figsize=(14, 12), facecolor='#0e1117')
    gs = gridspec.GridSpec(4, 1, height_ratios=[3, 1.5, 1.2, 1.0], hspace=0.12)

    # Panel 1: Price
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(time_hours, state.price_history, label="Mark Price", color='#00b4d8', linewidth=2.2)
    if oracle_prices and len(oracle_prices) >= n:
        ax1.plot(time_hours, oracle_prices[:n], label="Oracle Price", color='#ff9f1c', linestyle='--', linewidth=1.5)

    ax1.set_ylabel("Price", color='white')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.25, color='gray')

    # Liq volume secondary
    if liquidation_volumes:
        ax1_vol = ax1.twinx()
        vol = liquidation_volumes[:n]
        ax1_vol.bar(time_hours, vol, color='#ff4d4d', alpha=0.25, width=dt / 3600, label="Liq Volume")
        ax1_vol.set_ylabel("Liquidation Volume (SOL)", color='#ff4d4d')
        ax1_vol.tick_params(axis='y', labelcolor='#ff4d4d')

    # Panel 2: Premium (clean line)
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    if oracle_prices and len(oracle_prices) >= n:
        premium = np.array(state.price_history) - np.array(oracle_prices[:n])
        ax2.plot(time_hours, premium, color='#c77dff', linewidth=0.3, label="Premium (Mark - Oracle)")
        ax2.axhline(0, color='white', linestyle='--', alpha=0.5)
    ax2.set_ylabel("Premium", color='white')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.25, color='gray')

    # Panel 3: Funding Rate
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    if funding_history:
        funding_steps = np.arange(len(funding_history)) * (funding_interval / dt) * dt / 3600
        ax3.plot(funding_steps, funding_history, color='#4ade80', linewidth=1.9)
        ax3.axhline(0, color='white', linestyle='--', alpha=0.5)
    ax3.set_ylabel("Funding Rate", color='white')
    ax3.grid(True, alpha=0.25, color='gray')

    # Panel 4: Liq Count
    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    if liquidation_times:
        bin_size_hours = 0.5
        bins = np.arange(0, time_hours[-1] + bin_size_hours, bin_size_hours)
        counts, _ = np.histogram(np.array(liquidation_times) * dt / 3600, bins=bins)
        ax4.bar(bins[:-1], counts, width=bin_size_hours * 0.8, color='#ff4d4d', alpha=0.85)
    ax4.set_ylabel("Liq Count", color='white')
    ax4.set_xlabel("Time (hours)")
    ax4.grid(True, alpha=0.25, color='gray')

    # Hide upper x labels
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)

    fig.suptitle("Market Dashboard — Price, Premium, Funding & Liquidations", fontsize=14, color='white')
    plt.tight_layout()
    plt.show()

def plot_price_path(state, oracle_prices=None, liquidation_times=None, liquidation_volumes=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    n = len(state.price_history)
    steps = range(n)

    # === PRICE LINES ===
    ax1.plot(steps, state.price_history, label="Mark Price", color='blue', linewidth=1.0)

    # Fix length mismatch for Oracle Price
    if oracle_prices:
        if len(oracle_prices) == n - 1:
            oracle_prices = [state.price_history[0]] + oracle_prices  # align
        if len(oracle_prices) == n:
            ax1.plot(steps, oracle_prices, label="Oracle Price", color='orange', linestyle='--', linewidth=0.8,
                     alpha=0.9)

    ax1.set_ylabel("Price", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)

    # === LIQUIDATION VOLUME (secondary axis) ===
    if liquidation_volumes:
        vol = liquidation_volumes[:n]
        ax1_vol = ax1.twinx()
        ax1_vol.bar(steps, vol, color='red', alpha=0.18, width=10, label="Liq Volume")
        ax1_vol.set_ylabel("Liquidation Volume (SOL)", color='red')
        ax1_vol.tick_params(axis='y', labelcolor='red')

    ax1.set_title("Price Path (Mark vs Oracle) + Liquidation Volume")
    ax1.legend(loc='upper left')

    # === BOTTOM: NUMBER OF LIQUIDATIONS ===
    if liquidation_times:
        bin_size = 200
        bins = np.arange(0, n + bin_size, bin_size)
        counts, _ = np.histogram(liquidation_times, bins=bins)
        ax2.bar(bins[:-1], counts, width=bin_size * 0.8, color='red', alpha=0.75)
        ax2.set_ylabel("Number of Liquidations")
        ax2.set_xlabel("Time Step")
        ax2.grid(True)

    plt.tight_layout()
    plt.show()

def plot_funding_rate(funding_history):
    """Plot funding rate over time"""
    plt.figure(figsize=(12, 5))
    plt.plot(funding_history)
    plt.title("Funding Rate Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Funding Rate")
    plt.grid(True)
    plt.show()


# def plot_mm_pnl_over_time(mm_pnl_history):
#     """Individual Market Maker PnL over time"""
#     plt.figure(figsize=(12, 6))
#     for agent_id, pnl_series in mm_pnl_history.items():
#         plt.plot(pnl_series, label=f"MM {agent_id}")
#     plt.title("Market Maker PnL Over Time")
#     plt.xlabel("Time Step")
#     plt.ylabel("Cumulative PnL")
#     plt.legend()
#     plt.grid(True)
#     plt.show()


def plot_mm_pnl_over_time(mm_pnl_history):
    plt.figure(figsize=(12, 6))

    for agent_id, pnl_series in mm_pnl_history.items():
        # Downsample heavily for clarity
        if len(pnl_series) > 800:
            indices = np.linspace(0, len(pnl_series) - 1, 800, dtype=int)
            x = indices
            y = np.array(pnl_series)[indices]
        else:
            x = range(len(pnl_series))
            y = pnl_series

        plt.plot(x, y, label=f"MM {agent_id}", linewidth=1.4, alpha=0.85)

    plt.title("Market Maker PnL Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Cumulative PnL")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_equity_curve(total_pnl_history):
    """Cumulative total PnL over time"""
    plt.figure(figsize=(12, 6))
    cumulative = np.cumsum(total_pnl_history)
    plt.plot(cumulative)
    plt.title("Equity Curve (Total PnL)")
    plt.xlabel("Time Step")
    plt.ylabel("Cumulative PnL")
    plt.grid(True)
    plt.show()


def plot_drawdown(total_pnl_history):
    """Drawdown over time"""
    plt.figure(figsize=(12, 6))
    cumulative = np.cumsum(total_pnl_history)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = cumulative - running_max
    plt.plot(drawdown)
    plt.title("Drawdown Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.show()


def print_final_summary(position_manager):
    """Print final PnL summary"""
    pnls = [pos.realized_pnl + pos.unrealized_pnl for pos in position_manager.positions.values()]
    print("\n=== Final Summary ===")
    print(f"Total PnL: {sum(pnls):.2f}")
    print(f"Mean PnL per Agent: {np.mean(pnls):.2f}")
    print(f"Number of Open Positions: {len(pnls)}")


def plot_inventory_over_time(inventory_history):
    plt.figure(figsize=(12, 6))
    for agent_id, inv_series in inventory_history.items():
        plt.plot(inv_series, label=f"MM {agent_id}")
    plt.title("Market Maker Inventory Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Inventory (positive = long)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_orderbook_depth(snapshots):
    if not snapshots:
        return
    plt.figure(figsize=(12, 6))
    # Each snapshot is every 100 steps
    times = np.arange(len(snapshots)) * 100
    bid = [s[0] for s in snapshots]
    ask = [s[1] for s in snapshots]
    plt.plot(times, bid, label="Bid Depth (top 5)", color='green')
    plt.plot(times, ask, label="Ask Depth (top 5)", color='red')
    plt.title("Order Book Depth Over Time (sampled every 100 steps)")
    plt.xlabel("Time Step")
    plt.ylabel("Total Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_spread_over_time(spread_history):
    if not spread_history:
        return
    plt.figure(figsize=(12, 5))
    times = np.arange(len(spread_history)) * 100   # sampled every 100 steps
    plt.plot(times, spread_history, color='purple', linewidth=1.5)
    plt.title("Bid-Ask Spread Over Time (sampled every 100 steps)")
    plt.xlabel("Time Step")
    plt.ylabel("Spread")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_imbalance(imbalance_history):
    if not imbalance_history:
        return
    plt.figure(figsize=(12, 5))
    times = np.arange(len(imbalance_history)) * 100
    plt.plot(times, imbalance_history, color='teal', linewidth=1.5)
    plt.title("Order Book Imbalance Over Time (sampled every 100 steps)")
    plt.xlabel("Time Step")
    plt.ylabel("Imbalance Ratio")
    plt.axhline(0, color='black', linestyle='--', alpha=0.5)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def plot_imbalance(imbalance_history):
    """Order book imbalance over time"""
    if not imbalance_history:
        return
    plt.figure(figsize=(12, 5))
    plt.plot(imbalance_history, color='teal', linewidth=1.5)
    plt.title("Order Book Imbalance Over Time (Bid - Ask)")
    plt.xlabel("Time Step")
    plt.ylabel("Imbalance Ratio")
    plt.axhline(0, color='black', linestyle='--', alpha=0.5)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_sharpe_sortino(mm_pnl_history):
    """Combined Sharpe + Sortino bar chart"""
    sharpes = {}
    sortinos = {}

    for aid, pnl_series in mm_pnl_history.items():
        if len(pnl_series) < 50:
            sharpes[aid] = 0
            sortinos[aid] = 0
            continue

        returns = np.diff(pnl_series)
        mean_ret = np.mean(returns)

        # Sharpe
        if np.std(returns) > 1e-8:
            sharpes[aid] = mean_ret / np.std(returns) * np.sqrt(252 * 24)  # rough annualization
        else:
            sharpes[aid] = 0

        # Sortino (downside only)
        downside = returns[returns < 0]
        if len(downside) > 5 and np.std(downside) > 1e-8:
            sortinos[aid] = mean_ret / np.std(downside) * np.sqrt(252 * 24)
        else:
            sortinos[aid] = 0

    # Plot
    labels = [f"MM {aid}" for aid in sharpes.keys()]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width / 2, list(sharpes.values()), width, label='Sharpe Ratio', color='skyblue')
    ax.bar(x + width / 2, list(sortinos.values()), width, label='Sortino Ratio', color='salmon')

    ax.set_ylabel('Risk-Adjusted Return')
    ax.set_title('Sharpe & Sortino Ratios per Market Maker')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y')
    plt.tight_layout()
    plt.show()