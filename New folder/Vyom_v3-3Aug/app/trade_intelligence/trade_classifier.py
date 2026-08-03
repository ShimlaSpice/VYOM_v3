"""
Trade Classifier for VYOM.
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

        category = "AVOID"

        confidence = 40

        reasons: list[str] = []

        if (

            score >= 80

            and trend == "BULLISH"

            and sentiment in (

                "POSITIVE",

                "VERY_POSITIVE",

            )

        ):

            category = "POSITIONAL"

            confidence = 95

            reasons.extend(

                [

                    "Excellent technical structure.",

                    "Bullish market trend.",

                    "Positive news sentiment.",

                    "Suitable for positional trading.",

                ]

            )

        elif (

            score >= 65

            and trend == "BULLISH"

        ):

            category = "SWING"

            confidence = 85

            reasons.extend(

                [

                    "Strong bullish trend.",

                    "Good momentum.",

                    "Swing opportunity detected.",

                ]

            )

        elif (

            score >= 45

            and atr_percent >= 1.0

        ):

            category = "INTRADAY"

            confidence = 75

            reasons.extend(

                [

                    "Good intraday volatility.",

                    "Suitable for short-term trade.",

                ]

            )

        elif score >= 30:

            category = "WATCH"

            confidence = 60

            reasons.extend(

                [

                    "Needs confirmation.",

                    "Keep on watchlist.",

                ]

            )

        else:

            category = "AVOID"

            confidence = 35

            reasons.extend(

                [

                    "Weak technical setup.",

                    "Low probability trade.",

                ]

            )

        return {

            "category": category,

            "confidence": confidence,

            "reasons": reasons,

        }