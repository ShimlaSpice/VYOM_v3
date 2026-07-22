"""
Market data models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Quote:
    symbol: str
    last_price: float
    open_price: float
    high_price: float
    low_price: float
    volume: int
    timestamp: datetime


@dataclass(slots=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int