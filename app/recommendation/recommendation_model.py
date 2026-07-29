"""
Recommendation Model.
"""

from dataclasses import dataclass
from dataclasses import field


@dataclass
class Recommendation:

    # ---------------- Identity ----------------

    symbol: str

    recommendation: str

    category: str

    confidence: int

    probability: int = 0

    conviction: str = "UNKNOWN"

    # ---------------- Prices ----------------

    open: float = 0.0

    high: float = 0.0

    low: float = 0.0

    close: float = 0.0

    previous_close: float = 0.0

    change: float = 0.0

    change_percent: float = 0.0

    volume: int = 0

    # ---------------- Trade ----------------

    entry: float = 0.0

    stop_loss: float = 0.0

    target1: float = 0.0

    target2: float = 0.0

    exit_price: float = 0.0

    holding_days: int = 0

    # ---------------- Risk ----------------

    risk_reward: float = 0.0

    risk_level: str = "MEDIUM"

    atr: float = 0.0

    volatility: float = 0.0

    # ---------------- Company ----------------

    sector: str = ""

    industry: str = ""

    market_cap: float = 0.0

    pe: float = 0.0

    eps: float = 0.0

    roe: float = 0.0

    debt_to_equity: float = 0.0

    # ---------------- Position Sizing ----------------

    capital: float = 0.0

    quantity: int = 0

    expected_profit: float = 0.0

    maximum_loss: float = 0.0

    # ---------------- AI ----------------

    reasons: list[str] = field(

        default_factory=list,

    )

    ai_summary: str = ""

    scores: dict = field(

        default_factory=dict,

    )