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
    price: float = 0.0
    score: int = 0
    category: str = ""
    market: str = "NSE"
    change: float = 0.0
    change_percent: float = 0.0
    volume: int = 0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    previous_close: float = 0.0
    sector: str = ""
    industry: str = ""
    atr: float = 0.0
    risk_reward: float = 0.0
    ai_summary: str = ""
    reasons: list[str] = field(default_factory=list)
    scores: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_recommendation(cls, recommendation: Any) -> "RankedStock":
        """Build a RankedStock from a Recommendation-shaped object
        (duck-typed: anything with these attributes works)."""
        return cls(
            symbol=getattr(recommendation, "symbol", ""),
            recommendation=getattr(recommendation, "recommendation", "HOLD"),
            confidence=getattr(recommendation, "confidence", 0),
            probability=getattr(recommendation, "probability", 0),
            entry=getattr(recommendation, "entry", 0.0),
            stop_loss=getattr(recommendation, "stop_loss", 0.0),
            target1=getattr(recommendation, "target1", 0.0),
            target2=getattr(recommendation, "target2", 0.0),
            risk_level=getattr(recommendation, "risk_level", "MEDIUM"),
            price=getattr(recommendation, "close", getattr(recommendation, "price", 0.0)),
            score=getattr(recommendation, "score", 0),
            category=getattr(recommendation, "category", ""),
            market=getattr(recommendation, "market", "NSE"),
            change=getattr(recommendation, "change", 0.0),
            change_percent=getattr(recommendation, "change_percent", 0.0),
            volume=getattr(recommendation, "volume", 0),
            open=getattr(recommendation, "open", 0.0),
            high=getattr(recommendation, "high", 0.0),
            low=getattr(recommendation, "low", 0.0),
            close=getattr(recommendation, "close", 0.0),
            previous_close=getattr(recommendation, "previous_close", 0.0),
            sector=getattr(recommendation, "sector", ""),
            industry=getattr(recommendation, "industry", ""),
            atr=getattr(recommendation, "atr", 0.0),
            risk_reward=getattr(recommendation, "risk_reward", 0.0),
            ai_summary=getattr(recommendation, "ai_summary", ""),
            reasons=list(getattr(recommendation, "reasons", []) or []),
            scores=dict(getattr(recommendation, "scores", {}) or {}),
        )