# agents/taker.py
"""
Taker Agents
"""

import numpy as np

class Taker:
    def __init__(self, agent_id: int, strategy_type: str = "random", base_size: float = 5.0):
        self.agent_id = agent_id
        self.strategy_type = strategy_type
        self.base_size = base_size

    def get_order(self, mid_price: float, volatility: float = 0.0, trend: float = 0.0):
        """Return (side, price, size)"""
        size = self.base_size * (0.5 + np.random.random())

        if self.strategy_type == "random":
            side = 'buy' if np.random.random() < 0.5 else 'sell'
            price = mid_price * (1 + np.random.normal(0, volatility * 2))
        elif self.strategy_type == "momentum":
            side = 'buy' if trend > 0 else 'sell'
            price = mid_price * (1 + trend * 0.5)
        elif self.strategy_type == "mean_reversion":
            side = 'sell' if trend > 0 else 'buy'
            price = mid_price * (1 - trend * 0.5)
        else:
            side = 'buy' if np.random.random() < 0.5 else 'sell'
            price = mid_price

        return side, price, size