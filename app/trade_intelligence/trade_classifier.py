"""
Trade Classifier for VYOM.

Classifies every stock as:

- INTRADAY
- SWING
- POSITIONAL
- AVOID
"""

from __future__ import annotations


class TradeClassifier:

    def classify(
        self,
        score: int,
        atr_percent: float,
        trend: str,
        sentiment: str,
    ) -> dict:

        reasons: list[str] = []

        category = "AVOID"

        confidence = 40

        # --------------------------------------------------
        # POSITIONAL
        # --------------------------------------------------

        if (
            score >= 80
            and trend == "BULLISH"
            and sentiment == "POSITIVE"
        ):

            category = "POSITIONAL"

            confidence = 95

            reasons.extend(
                [
                    "Strong technical score.",
                    "Bullish market trend.",
                    "Positive news sentiment.",
                    "Suitable for long-term holding.",
                ]
            )

        # --------------------------------------------------
        # SWING
        # --------------------------------------------------

        elif (
            score >= 60
            and trend == "BULLISH"
        ):

            category = "SWING"

            confidence = 85

            reasons.extend(
                [
                    "Bullish trend detected.",
                    "Good technical strength.",
                    "Swing opportunity available.",
                ]
            )

        # --------------------------------------------------
        # INTRADAY
        # --------------------------------------------------

        elif (
            score >= 45
            and atr_percent >= 1.5
        ):

            category = "INTRADAY"

            confidence = 75

            reasons.extend(
                [
                    "High daily movement.",
                    "Enough volatility for intraday.",
                ]
            )

        # --------------------------------------------------
        # WATCHLIST
        # --------------------------------------------------

        elif score >= 30:

            category = "WATCH"

            confidence = 60

            reasons.extend(
                [
                    "Keep under observation.",
                    "Needs confirmation.",
                ]
            )

        # --------------------------------------------------
        # AVOID
        # --------------------------------------------------

        else:

            category = "AVOID"

            confidence = 40

            reasons.extend(
                [
                    "Weak technical structure.",
                    "Low probability setup.",
                ]
            )

        return {

            "category": category,

            "confidence": confidence,

            "reasons": reasons,

        }