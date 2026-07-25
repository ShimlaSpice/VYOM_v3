"""
ATR Engine for VYOM.

Calculates:
- True Range
- Average True Range
- ATR %
- Volatility
"""

from __future__ import annotations

import math


class ATREngine:

    def calculate(

        self,

        highs: list[float],

        lows: list[float],

        closes: list[float],

        period: int = 14,

    ) -> float:

        if (

            len(highs) < period + 1

            or len(lows) < period + 1

            or len(closes) < period + 1

        ):

            return 0.0

        true_ranges = []

        for i in range(1, len(closes)):

            try:

                high = float(highs[i])

                low = float(lows[i])

                previous_close = float(closes[i - 1])

            except Exception:

                continue

            if any(

                math.isnan(x)

                for x in [

                    high,

                    low,

                    previous_close,

                ]

            ):

                continue

            tr = max(

                high - low,

                abs(high - previous_close),

                abs(low - previous_close),

            )

            true_ranges.append(

                tr,

            )

        if len(true_ranges) < period:

            return 0.0

        atr = sum(

            true_ranges[-period:]

        ) / period

        if math.isnan(atr):

            return 0.0

        return round(

            atr,

            2,

        )

    def volatility(

        self,

        atr: float,

        price: float,

    ) -> str:

        if (

            price <= 0

            or atr <= 0

        ):

            return "UNKNOWN"

        atr_percent = (

            atr / price

        ) * 100

        if atr_percent < 1:

            return "LOW"

        if atr_percent < 2.5:

            return "MEDIUM"

        return "HIGH"

    def summary(

        self,

        highs: list[float],

        lows: list[float],

        closes: list[float],

        period: int = 14,

    ) -> dict:

        atr = self.calculate(

            highs,

            lows,

            closes,

            period,

        )

        price = closes[-1] if closes else 0.0

        if (

            price <= 0

            or math.isnan(price)

        ):

            atr_percent = 0.0

        else:

            atr_percent = round(

                (atr / price) * 100,

                2,

            )

        return {

            "atr": atr,

            "price": round(

                price,

                2,

            ),

            "atr_percent": atr_percent,

            "volatility": self.volatility(

                atr,

                price,

            ),

        }