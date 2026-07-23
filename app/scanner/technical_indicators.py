"""
Technical Indicators Engine for VYOM.
"""

from __future__ import annotations

from statistics import mean


class TechnicalIndicators:
    """
    Collection of technical analysis calculations.
    """

    @staticmethod
    def sma(values: list[float], period: int) -> float:
        if len(values) < period:
            return 0.0
        return mean(values[-period:])

    @staticmethod
    def ema(values: list[float], period: int) -> float:
        if len(values) < period:
            return 0.0

        multiplier = 2 / (period + 1)
        ema = values[0]

        for price in values[1:]:
            ema = ((price - ema) * multiplier) + ema

        return ema

    @staticmethod
    def price_change(current: float, previous: float) -> float:
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def rsi(closes: list[float], period: int = 14) -> float:

        if len(closes) < period + 1:
            return 50.0

        gains = []
        losses = []

        for i in range(1, period + 1):
            change = closes[-period - 1 + i] - closes[-period - 2 + i]

            if change >= 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))


    @staticmethod
    def macd(
        closes: list[float],
    ) -> tuple[float, float]:

        if len(closes) < 35:
            return 0.0, 0.0

        ema12 = TechnicalIndicators.ema(closes, 12)
        ema26 = TechnicalIndicators.ema(closes, 26)

        macd = ema12 - ema26

        signal = macd

        return macd, signal

    @staticmethod
    def average_volume(
        volumes: list[int],
        period: int = 20,
    ) -> float:

        if len(volumes) < period:
            return 0.0

        return sum(volumes[-period:]) / period
    
    @staticmethod
    def breakout(
        highs: list[float],
        current_close: float,
        period: int = 20,
    ) -> bool:

        if len(highs) < period:
            return False

        resistance = max(highs[-period:])

        return current_close >= resistance