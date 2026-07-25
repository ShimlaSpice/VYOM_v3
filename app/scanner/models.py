"""
Scanner Domain Models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ScanCandidate:

    symbol: str

    score: int = 0

    decision: str = "HOLD"

    confidence: float = 0.0

    reasons: list[str] = field(

        default_factory=list,

    )

    indicators: dict[str, Any] = field(

        default_factory=dict,

    )

    price: float = 0.0

    volume: int = 0

    rsi: float = 0.0

    macd: float = 0.0

    sma20: float = 0.0

    sma50: float = 0.0

    ema20: float = 0.0

    atr: float = 0.0

    relative_strength: float = 0.0

    sector: str = ""

    industry: str = ""

    pe: float | None = None

    eps: float | None = None

    roe: float | None = None

    debt_to_equity: float | None = None

    market_cap: int = 0

    breakout: bool = False

    average_volume: float = 0.0


@dataclass(slots=True)
class ScanResult:

    generated_at: str

    candidates: list[ScanCandidate] = field(

        default_factory=list,

    )