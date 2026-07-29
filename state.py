# state.py
"""
Central Simulation State

Single source of truth for the entire simulation.
Uses a class for high-level organization + NumPy for performance-critical data.
"""
"""
Central Simulation State
"""

from dataclasses import dataclass
import numpy as np
from typing import Optional
from order_book import OrderBook
from positions import PositionManager


@dataclass
class SimulationState:
    timestamp: float
    order_book: OrderBook
    position_manager: PositionManager

    price_history: np.ndarray
    history_index: int = 0

    @classmethod
    def create_initial_state(cls, config):
        ob = OrderBook(config.TICK_SIZE)

        num_steps = int(config.SIM_DURATION / config.DT) + 2   # safety margin
        price_history = np.zeros(num_steps-1)
        price_history[0] = config.INITIAL_PRICE

        return cls(
            timestamp=0.0,
            order_book=ob,
            position_manager=PositionManager(),
            price_history=price_history,
            history_index=1   # start after initial price
        )

    def record_price(self, price: float):
        if self.history_index < len(self.price_history):
            self.price_history[self.history_index] = price
            self.history_index += 1