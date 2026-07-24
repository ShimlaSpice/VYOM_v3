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

            }

        sma20 = sum(closes[-20:]) / 20

        sma50 = sum(closes[-50:]) / 50

        latest = closes[-1]

        # ----------------------------

        if latest > sma20 > sma50:

            return {

                "trend": "BULLISH",

                "score": 10,

            }

        elif latest > sma20:

            return {

                "trend": "SIDEWAYS",

                "score": 7,

            }

        else:

            return {

                "trend": "BEARISH",

                "score": 3,

            }