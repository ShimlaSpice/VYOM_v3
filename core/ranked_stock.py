from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RankedStock:

    symbol: str

    score: float = 0.0

    rank: int = 0

    recommendation: str = "HOLD"

    confidence: float = 0.0

    probability: float = 0.0

    conviction: float = 0.0

    close: float = 0.0

    ltp: float = 0.0

    change_percent: float = 0.0

    volume: int = 0

    atr: float = 0.0

    rsi: float = 0.0

    macd: float = 0.0

    sma20: float = 0.0

    ema20: float = 0.0

    target: float = 0.0

    stop_loss: float = 0.0

    risk_reward: float = 0.0

    sector: str = ""

    reason: str = ""

    summary: str = ""

    trade_plan: str = ""

    jarvis: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):

        if self.ltp == 0:

            self.ltp = self.close

        elif self.close == 0:

            self.close = self.ltp