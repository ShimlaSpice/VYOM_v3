"""
Shared Market Context.

Carries market data and indicators across the entire VYOM pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd


@dataclass(slots=True)
class MarketContext:

    symbol: str

    dataframe: pd.DataFrame

    indicators: dict = field(default_factory=dict)

    open: float = 0.0

    high: float = 0.0

    low: float = 0.0

    close: float = 0.0

    previous_close: float = 0.0

    ltp: float = 0.0

    volume: int = 0

    timestamp: datetime | None = None

    latest_candle: dict = field(default_factory=dict)

    fundamentals: dict = field(default_factory=dict)

    news: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_dataframe(
        cls,
        symbol: str,
        dataframe: pd.DataFrame,
        indicators: dict,
        fundamentals: dict | None = None,
        news: dict | None = None,
    ) -> "MarketContext":

        latest = dataframe.iloc[-1]

        previous_close = (
            float(dataframe["Close"].iloc[-2])
            if len(dataframe) > 1
            else float(latest["Close"])
        )

        return cls(

            symbol=symbol,

            dataframe=dataframe,

            indicators=indicators,

            open=float(latest["Open"]),

            high=float(latest["High"]),

            low=float(latest["Low"]),

            close=float(latest["Close"]),

            previous_close=previous_close,

            ltp=float(latest["Close"]),

            volume=int(latest["Volume"]),

            timestamp=dataframe.index[-1].to_pydatetime(),

            latest_candle={

                "open": float(latest["Open"]),

                "high": float(latest["High"]),

                "low": float(latest["Low"]),

                "close": float(latest["Close"]),

                "volume": int(latest["Volume"]),

            },

            fundamentals=fundamentals or {},

            news=news or {},

        )

    @property
    def change(self) -> float:

        return self.close - self.previous_close

    @property
    def change_percent(self) -> float:

        if self.previous_close == 0:
            return 0.0

        return round(

            (self.change / self.previous_close) * 100,

            2,

        )

    def to_dict(self) -> dict:

        return {

            "symbol": self.symbol,

            "open": self.open,

            "high": self.high,

            "low": self.low,

            "close": self.close,

            "previous_close": self.previous_close,

            "ltp": self.ltp,

            "change": self.change,

            "change_percent": self.change_percent,

            "volume": self.volume,

            "timestamp": self.timestamp,

            "latest_candle": self.latest_candle,

            "indicators": self.indicators,

            "fundamentals": self.fundamentals,

            "news": self.news,

            "metadata": self.metadata,

        }