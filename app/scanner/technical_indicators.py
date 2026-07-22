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