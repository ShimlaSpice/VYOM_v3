"""
Scanner domain models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ScanCandidate:
    symbol: str
    score: float = 0.0
    decision: str = "HOLD"
    confidence: float = 0.0
    reasons: list[str] = field(default_factory=list)
    indicators: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ScanResult:
    generated_at: str
    candidates: list[ScanCandidate] = field(default_factory=list)