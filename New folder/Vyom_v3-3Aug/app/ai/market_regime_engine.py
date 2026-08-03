"""
Market Regime Engine for VYOM.

Identifies the current market regime.

Jarvis should behave differently in:

- Trending Market
- Range-bound Market
- Volatile Market
- Bear Market
- Bull Market
"""

from __future__ import annotations


class MarketRegimeEngine:

    def analyze(

        self,

        adx: float,

        rsi: float,

        atr_percent: float,

        market_trend: str,

    ) -> dict:

        regime = "UNKNOWN"

        score = 0

        reasons = []

        # -------------------------------------
        # Strong Bull Market
        # -------------------------------------

        if (

            market_trend == "BULLISH"

            and adx >= 25

            and rsi >= 55

            and atr_percent < 3

        ):

            regime = "BULL"

            score = 10

            reasons.append(

                "Strong Bull Market"

            )

        # -------------------------------------
        # Strong Bear Market
        # -------------------------------------

        elif (

            market_trend == "BEARISH"

            and adx >= 25

            and rsi <= 45

        ):

            regime = "BEAR"

            score = 2

            reasons.append(

                "Strong Bear Market"

            )

        # -------------------------------------
        # Range Market
        # -------------------------------------

        elif adx < 20:

            regime = "RANGE"

            score = 5

            reasons.append(

                "Range Bound Market"

            )

        # -------------------------------------
        # Volatile Market
        # -------------------------------------

        elif atr_percent >= 4:

            regime = "VOLATILE"

            score = 4

            reasons.append(

                "High Volatility"

            )

        # -------------------------------------
        # Trending Market
        # -------------------------------------

        else:

            regime = "TRENDING"

            score = 8

            reasons.append(

                "Healthy Trending Market"

            )

        # -------------------------------------

        if regime == "BULL":

            advice = "Trend Following"

        elif regime == "BEAR":

            advice = "Avoid Long Positions"

        elif regime == "RANGE":

            advice = "Trade Support & Resistance"

        elif regime == "VOLATILE":

            advice = "Reduce Position Size"

        else:

            advice = "Trade With Trend"

        return {

            "regime": regime,

            "score": score,

            "advice": advice,

            "reasons": reasons,

        }