"""
Market Trend Engine.

Determines overall market trend.
"""

from __future__ import annotations


class MarketTrendEngine:

    def evaluate(

        self,

        closes: list[float],

    ) -> dict:

        if len(closes) < 50:

            return {

                "trend": "UNKNOWN",

                "score": 5,

                "strength": 0,

                "sma20": None,

                "sma50": None,

                "reason": "Insufficient data",

            }

        sma20 = sum(closes[-20:]) / 20

        sma50 = sum(closes[-50:]) / 50

        latest = closes[-1]

        strength = round(

            abs(sma20 - sma50) / sma50 * 100,

            2,

        )

        if latest > sma20 > sma50:

            trend = "BULLISH"

            score = 10

            reason = "Price above SMA20 and SMA50"

        elif latest > sma20 and sma20 <= sma50:

            trend = "RECOVERING"

            score = 8

            reason = "Price above SMA20"

        elif latest < sma20 < sma50:

            trend = "BEARISH"

            score = 2

            reason = "Price below SMA20 and SMA50"

        else:

            trend = "SIDEWAYS"

            score = 5

            reason = "No clear trend"

        return {

            "trend": trend,

            "score": score,

            "strength": strength,

            "sma20": round(sma20, 2),

            "sma50": round(sma50, 2),

            "reason": reason,

        }