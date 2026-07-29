# oracle.py
"""
Oracle & Mark Price System

Simulates realistic oracle behavior with smoothing and noise.
"""

import numpy as np

class Oracle:
    def __init__(self, initial_price: float, noise_std: float = 0.0003, ema_alpha: float = 0.01):
        self.oracle_price = initial_price
        self.last_mid_price = initial_price
        self.noise_std = noise_std
        self.ema_alpha = ema_alpha

    def update(self, external_price: float, sim_mid_price: float):
        """Update oracle and compute mark price"""
        # Add small noise to external price
        self.oracle_price = external_price * (1 + np.random.normal(0, self.noise_std))

        # EMA smoothing for mark price
        self.last_mid_price = (1 - self.ema_alpha) * self.last_mid_price + self.ema_alpha * sim_mid_price

        # Mark price = blend of oracle + smoothed on-chain mid
        mark_price = (self.oracle_price + self.last_mid_price) / 2
        return mark_price, self.oracle_price