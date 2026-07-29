# metrics.py
"""
Metrics and Analysis for Simulation Results
"""

import numpy as np


def calculate_pnl_summary(position_manager):
    """Basic PnL summary"""
    if not position_manager.positions:
        return {"total_pnl": 0.0, "num_positions": 0}

    pnls = [pos.realized_pnl + pos.unrealized_pnl for pos in position_manager.positions.values()]
    return {
        "total_pnl": sum(pnls),
        "mean_pnl": np.mean(pnls),
        "std_pnl": np.std(pnls),
        "num_positions": len(pnls),
        "max_pnl": max(pnls) if pnls else 0,
        "min_pnl": min(pnls) if pnls else 0
    }


def print_simulation_summary(state, position_manager):
    """Print useful summary"""
    print("\n=== Simulation Summary ===")
    final_price = state.price_history[state.history_index - 1] if state.history_index > 0 else state.price_history[
        0]
    print(f"Final Price: {final_price:.2f}")
    print(f"Number of Open Positions: {len(position_manager.positions)}")

    summary = calculate_pnl_summary(position_manager)
    print(f"Total PnL: {summary['total_pnl']:.2f}")
    print(f"Mean PnL: {summary['mean_pnl']:.2f}")
    print(f"Std PnL: {summary['std_pnl']:.2f}")