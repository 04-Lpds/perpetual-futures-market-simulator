# funding.py
"""
Copmutes 8 hour rate but settles hourly, like HyperLiquid
"""
import numpy as np


def sample_premium(premium_samples: list, mark_price: float, oracle_price: float):
    """Add current premium"""
    premium = mark_price - oracle_price
    premium_samples.append(premium)
    if len(premium_samples) > 1000:  # safety cap
        premium_samples.pop(0)


def calculate_hourly_funding(premium_samples: list, config) -> float:
    """Configurable funding calculation"""
    if len(premium_samples) < 30:
        return 0.0

    # Rolling window
    recent = premium_samples[-config.FUNDING_WINDOW:] if hasattr(config, 'FUNDING_WINDOW') else premium_samples[-300:]
    avg_premium = np.mean(recent)

    funding_rate = avg_premium * config.PREMIUM_SCALE_FACTOR

    # Clamp
    clamp = config.FUNDING_CLAMP if hasattr(config, 'FUNDING_CLAMP') else 0.0005
    funding_rate = max(-clamp, min(clamp, funding_rate))

    return funding_rate