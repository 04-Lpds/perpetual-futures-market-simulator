# agents/market_maker.py
"""
Market Maker Agents with Multiple Strategies

Designed for easy comparison of different MM approaches in Monte Carlo runs.
"""

import numpy as np
from typing import Tuple, List

class MarketMaker:
    def __init__(self, agent_id: int, strategy_type: str, base_spread_bps: float = 5.0,
                 max_inventory: float = 500.0):
        self.agent_id = agent_id
        self.strategy_type = strategy_type
        self.base_spread_bps = base_spread_bps
        self.max_inventory = max_inventory
        self.inventory = 0.0


    def get_quotes(self, mid_price: float, volatility: float = 0.0, trend: float = 0.0) -> Tuple[Optional[float], Optional[float]]:
        base_spread = (self.base_spread_bps / 10000.0) * mid_price

        if self.strategy_type == "inventory_aware":
            spread = base_spread
            skew = self.inventory * 0.0015   # stronger inventory skew
        elif self.strategy_type == "passive":
            spread = base_spread * 2.5
            skew = self.inventory * 0.0003
        elif self.strategy_type == "aggressive":
            spread = base_spread * 0.5
            skew = self.inventory * 0.0008
        elif self.strategy_type == "volatility_aware":
            spread = base_spread * (1 + volatility * 15)
            skew = 0.0
        elif self.strategy_type == "momentum":
            spread = base_spread * 0.8
            skew = trend * 0.0025
        elif self.strategy_type == "mean_reversion":
            spread = base_spread * 1.2
            skew = -trend * 0.0025
        else:
            spread = base_spread
            skew = 0.0

        # Stronger inventory control
        if abs(self.inventory) > self.max_inventory * 0.6:
            spread *= 3.0

        bid = mid_price - spread / 2 + skew
        ask = mid_price + spread / 2 + skew

        return bid, ask



    # def get_quotes(self, mid_price: float, volatility: float = 0.0, trend: float = 0.0) -> Tuple[Optional[float], Optional[float]]:
    #     """Return (bid_price, ask_price). None = no quote."""
    #     spread = (self.base_spread_bps / 10000.0) * mid_price
    #
    #     if self.strategy_type == "inventory_aware":
    #         skew = self.inventory * 0.0008
    #     elif self.strategy_type == "passive":
    #         spread *= 1.8
    #         skew = 0.0
    #     elif self.strategy_type == "aggressive":
    #         spread *= 0.6
    #         skew = self.inventory * 0.0003
    #     elif self.strategy_type == "volatility_aware":
    #         spread *= (1 + volatility * 10)  # Widen in high vol
    #         skew = 0.0
    #     elif self.strategy_type == "momentum":
    #         skew = trend * 0.001  # Follow short-term trend
    #     elif self.strategy_type == "mean_reversion":
    #         skew = -trend * 0.001  # Bet against trend
    #     else:  # default
    #         skew = 0.0
    #
    #     # Inventory safety
    #     if abs(self.inventory) > self.max_inventory * 0.7:
    #         spread *= 2.0
    #
    #     bid = mid_price - spread / 2 + skew
    #     ask = mid_price + spread / 2 + skew
    #
    #     return bid, ask

    def on_trade(self, size: float, taker_side: str):
        """Update inventory when your quote is filled"""
        if taker_side == 'buy':  # Taker bought from you → you sold
            self.inventory -= size
        else:  # Taker sold to you → you bought
            self.inventory += size