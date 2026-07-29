# config.py

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Config:
    # =====================
    # GENERAL / ASSET
    # =====================
    SYMBOL: str = "SOL"
    INITIAL_PRICE: float = 150.0
    SIM_RANDOM_SEED: int = 42
    PRICE_RANDOM_SEED: int = 29

    # =====================
    # ORDER BOOK PARAMETERS
    # =====================
    TICK_SIZE: float = 0.01          # Minimum price increment
    LOT_SIZE: float = 0.1            # Minimum size increment
    MAX_BOOK_DEPTH: int = 100        # Max price levels to track per side

    # =====================
    # SIMULATION PARAMETERS
    # =====================
    DT: float = 1.0                 # Simulation timestep (seconds)
    SIM_DURATION: float = 3600 * 8   # Total simulation time (e.g. 8 hours)
    WARMUP_STEPS: int = 300          # Steps before recording metrics

    # =====================
    # PLOTTING TOGGLES
    # =====================
    PLOT_PRICE_AND_LIQS: bool = True
    PLOT_FUNDING: bool = True
    PLOT_MM_PNL: bool = True
    PLOT_EQUITY_CURVE: bool = True
    PLOT_DRAWDOWN: bool = True
    PLOT_INVENTORY: bool = True
    PLOT_ORDERBOOK_DEPTH: bool = True
    PLOT_SPREAD: bool = True
    PLOT_IMBALANCE: bool = False
    PLOT_SHARPE_SORTINO: bool = False

    # =====================
    # MARKET MAKER AGENTS
    # =====================
    NUM_MARKET_MAKERS: int = 8
    MM_BASE_SPREAD_BPS: float = 4.0          # Base spread in basis points
    MM_INVENTORY_TARGET: float = 0.0         # Target inventory (0 = delta neutral)
    MM_MAX_INVENTORY: float = 500.0          # Max absolute inventory before pulling quotes
    MM_AGGRESSIVENESS: float = 1.0           # How tight they quote (higher = more aggressive)

    # Different MM strategy types
    MM_STRATEGY_TYPES: List[str] = None

    def __post_init__(self):
        if self.MM_STRATEGY_TYPES is None:
            self.MM_STRATEGY_TYPES: List[str] = [
                "inventory_aware",
                "passive",
                "aggressive",
                "volatility_aware",
                "momentum",
                "mean_reversion"
            ]
        if self.PRICE_SHOCK_SCENARIOS is None:
            self.PRICE_SHOCK_SCENARIOS = [-0.12, -0.06, 0.0, 0.06, 0.12]

    # =====================
    # TAKER / TRADER AGENTS
    # =====================
    NUM_TAKERS: int = 15
    TAKER_ORDER_SIZE_MEAN: float = 5.0
    TAKER_ORDER_SIZE_STD: float = 3.0
    TAKER_AGGRESSION_PROB: float = 0.3       # Probability a taker crosses the spread

    # =====================
    # LIQUIDATION PARAMETERS
    # =====================
    MAINTENANCE_MARGIN_RATE: float = 0.025   # 2.5%
    LIQUIDATION_PENALTY: float = 0.005       # 0.5% penalty on liquidation
    LIQUIDATION_THRESHOLD: float = 0.0       # Can add buffer if needed

    # =====================
    # FUNDING RATE
    # =====================
    FUNDING_INTERVAL: float = 3600           # Pay funding every hour (in seconds)
    FUNDING_PREMIUM_SAMPLING_RATE: float = 5 # Sample every 5 seconds for premium
    INTEREST_RATE_8H: float = 0.0001         # 0.01% per 8 hours
    FUNDING_CLAMP: float = 0.0005            # ±0.05%
    PREMIUM_SCALE_FACTOR = 3.5               # How stongly premium affects rates

    # =====================
    # ORACLE / MARK PRICE
    # =====================
    ORACLE_UPDATE_INTERVAL: float = 3.0      # Seconds between oracle updates
    ORACLE_NOISE_STD: float = 0.0003         # Small noise on oracle
    EMA_WINDOW_SECONDS: float = 150.0        # 150-second EMA for mark price
    EMA_ALPHA: float = 0.01

    # =====================
    # MARKET IMPACT & SLIPPAGE (Optional but useful)
    # =====================
    ENABLE_MARKET_IMPACT: bool = True
    IMPACT_COEFFICIENT: float = 0.00005      # How much size moves price

    # =====================
    # MONTE CARLO / EXPERIMENT
    # =====================
    NUM_MONTE_CARLO_RUNS: int = 50
    PRICE_SHOCK_SCENARIOS: List[float] = None  # e.g. [-0.15, -0.08, 0.0, 0.08, 0.15]

@dataclass
class PricePathConfig:
    initial_price: float = 150.0
    dt: float = 1.0
    num_steps: int = None          # Will be set from main config
    seed: Optional[int] = 42       # None = random each run
    regimes: List[dict] = None

    def __post_init__(self):
        if self.regimes is None:
            self.regimes = [
                {"mu": 0.00008, "sigma": 0.0006, "duration": 9000},   # Low vol up
                {"mu": -0.00005, "sigma": 0.0018, "duration": 9000},  # High vol crash
                {"mu": 0.00002, "sigma": 0.0007, "duration": 10800},  # Recovery / calm
            ]