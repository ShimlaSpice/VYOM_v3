"""
Market Trend Engine.
"""

from __future__ import annotations

from app.market import MarketDataProvider
from app.scanner.technical_indicators import TechnicalIndicators


class MarketTrendEngine:

    def __init__(self, provider: MarketDataProvider):

        self.provider = provider

    def analyze(self) -> dict:

        candles = self.provider.get_candles(
            symbol="^NSEI",
            interval="1d",
            limit=50,
        )

        closes = [c["close"] for c in candles]

        sma20 = TechnicalIndicators.sma(closes, 20)
        ema20 = TechnicalIndicators.ema(closes, 20)

        last = closes[-1]

        trend = "SIDEWAYS"

        if last > sma20 and last > ema20:
            trend = "BULLISH"

        elif last < sma20 and last < ema20:
            trend = "BEARISH"

        return {
            "trend": trend,
            "close": last,
            "sma20": sma20,
            "ema20": ema20,
        }