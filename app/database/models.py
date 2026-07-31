"""
Database Models for VYOM.

Typed records that map 1:1 onto SQLite tables. Each dataclass mirrors a
table's schema; `id` and `created_at` are populated by the repository
layer (id on read from DB, created_at at construction time) and should
not be set by callers building a new record by hand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


def _now_iso() -> str:
    """Current local timestamp as an ISO-8601 string, evaluated fresh
    for every record (unlike a bare default, which would only evaluate
    once at class-definition time)."""
    return datetime.now().isoformat()


@dataclass(slots=True)
class RecommendationRecord:
    symbol: str
    recommendation: str
    category: str
    confidence: int
    entry: float
    stop_loss: float
    target1: float
    target2: float
    risk_reward: float
    id: int | None = None
    created_at: str = field(default_factory=_now_iso)


@dataclass(slots=True)
class MarketSnapshot:
    symbol: str
    price: float
    volume: int
    rsi: float
    macd: float
    sma20: float
    sma50: float
    ema20: float
    id: int | None = None
    created_at: str = field(default_factory=_now_iso)


@dataclass(slots=True)
class TradeRecord:
    symbol: str
    side: str
    quantity: int
    entry_price: float
    exit_price: float = 0.0
    pnl: float = 0.0
    status: str = "OPEN"
    id: int | None = None
    created_at: str = field(default_factory=_now_iso)


@dataclass(slots=True)
class PortfolioRecord:
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    id: int | None = None
    created_at: str = field(default_factory=_now_iso)