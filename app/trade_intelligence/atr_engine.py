"""
ATR Engine for VYOM.

Calculates:
- True Range (TR)
- Average True Range (ATR)
- Volatility Classification
"""

from __future__ import annotations

from statistics import mean


class ATREngine:
    """
    Average True Range Engine.
    """

    def calculate(
        self,
        highs: list[float],
        lows: list[float],
        closes: list[float],
        period: int = 14,
    ) -> float:
        """
        Calculate ATR using Wilder's True Range.
        """

        if (
            len(highs) < period + 1
            or len(lows) < period + 1
            or len(closes) < period + 1
        ):
            return 0.0

        true_ranges: list[float] = []

        for i in range(1, len(closes)):

            high = highs[i]
            low = lows[i]
            previous_close = closes[i - 1]

            tr = max(
                high - low,
                abs(high - previous_close),
                abs(low - previous_close),
            )

            true_ranges.append(tr)

        return round(
            mean(true_ranges[-period:]),
            2,
        )

    def volatility(
        self,
        atr: float,
        price: float,
    ) -> str:
        """
        Classify stock volatility.
        """

        if price <= 0:
            return "UNKNOWN"

        percentage = (atr / price) * 100

        if percentage < 1:
            return "LOW"

        if percentage < 2.5:
            return "MEDIUM"

        return "HIGH"

    def summary(
        self,
        highs: list[float],
        lows: list[float],
        closes: list[float],
        period: int = 14,
    ) -> dict:
        """
        Complete ATR Analysis.
        """

        atr = self.calculate(
            highs,
            lows,
            closes,
            period,
        )

        price = closes[-1]

        return {
            "atr": atr,
            "price": round(price, 2),
            "atr_percent": round(
                (atr / price) * 100,
                2,
            ) if price else 0.0,
            "volatility": self.volatility(
                atr,
                price,
            ),
        }