"""
Relative Strength Engine.
"""

from __future__ import annotations


class RelativeStrength:

    @staticmethod
    def calculate(
        stock_change: float,
        market_change: float,
    ) -> float:

        return stock_change - market_change