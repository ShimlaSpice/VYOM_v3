"""
Top10 Models.

RankedStock is the curated, boundary-facing output of Top10Engine —
deliberately smaller than the internal Recommendation model it's built
from, since a UI or export target only needs the fields that actually
matter for "here's what to look at."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RankedStock:

    symbol: str
    recommendation: str
    confidence: int
    probability: int
    entry: float
    stop_loss: float
    target1: float
    target2: float
    risk_level: str
    reasons: list[str] = field(default_factory=list)

    @classmethod
    def from_recommendation(cls, recommendation: Any) -> "RankedStock":
        """Build a RankedStock from a Recommendation-shaped object
        (duck-typed: anything with these attributes works)."""
        return cls(
            symbol=recommendation.symbol,
            recommendation=recommendation.recommendation,
            confidence=recommendation.confidence,
            probability=recommendation.probability,
            entry=recommendation.entry,
            stop_loss=recommendation.stop_loss,
            target1=recommendation.target1,
            target2=recommendation.target2,
            risk_level=recommendation.risk_level,
            reasons=list(recommendation.reasons),
        )