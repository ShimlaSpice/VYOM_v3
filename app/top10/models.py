"""
Top10 Models.
"""

from dataclasses import dataclass, field


@dataclass
class RankedStock:

    symbol: str

    recommendation: str

    confidence: int

    score: int

    entry: float

    stop_loss: float

    target1: float

    target2: float

    risk_level: str

    reasons: list[str] = field(default_factory=list)