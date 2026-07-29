"""
Price Path Generator
Supports multiple stochastic processes and volatility regimes for realistic Monte Carlo testing.
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PricePathConfig:
    initial_price: float = 150.0
    dt: float = 1.0
    num_steps: int = 28800
    seed: int = 42

    # Regime parameters
    regimes: List[dict] = None  # list of dicts with mu, sigma, duration


class PricePathGenerator:
    def __init__(self, config: PricePathConfig):
        self.config = config
        np.random.seed(config.seed)

        if self.config.regimes is None:
            self.config.regimes = [
                {"mu": 0.00005, "sigma": 0.0008, "duration": 8000},  # Low vol uptrend
                {"mu": -0.00002, "sigma": 0.0015, "duration": 8000},  # High vol down
                {"mu": 0.00003, "sigma": 0.0006, "duration": 12800},  # Calm
            ]

    def generate_gbm(self, mu: float, sigma: float, num_steps: int) -> np.ndarray:
        """Geometric Brownian Motion"""
        dt = self.config.dt
        prices = np.zeros(num_steps + 1)
        prices[0] = self.config.initial_price

        for t in range(1, num_steps + 1):
            dW = np.random.normal(0, np.sqrt(dt))
            prices[t] = prices[t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * dW)

        return prices

    def generate_with_regimes(self) -> Tuple[np.ndarray, List[str]]:
        """Generate path with multiple volatility regimes"""
        full_path = []
        regime_labels = []
        current_price = self.config.initial_price

        for regime in self.config.regimes:
            mu = regime["mu"]
            sigma = regime["sigma"]
            steps = regime["duration"]

            path = self.generate_gbm(mu, sigma, steps)
            # Connect regimes smoothly
            if full_path:
                path = path * (full_path[-1] / path[0])

            full_path.extend(path[1:])  # avoid duplicating first point
            regime_labels.extend([f"regime_{mu:.5f}_{sigma:.4f}"] * steps)

        return np.array(full_path), regime_labels

    def generate_heston(self):
        """Placeholder - more advanced stochastic vol (can expand later)"""
        pass  # TODO: Heston model