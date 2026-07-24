"""
Recommendation Model.
"""

from dataclasses import dataclass, field


@dataclass
class Recommendation:

    symbol: str

    recommendation: str

    category: str

    confidence: int

    entry: float

    stop_loss: float

    target1: float

    target2: float

    risk_reward: float

    risk_level: str

    reasons: list[str] = field(default_factory=list)

    scores: dict = field(default_factory=dict)