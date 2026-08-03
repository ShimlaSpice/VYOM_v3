"""
News Intelligence Engine.
"""

from __future__ import annotations


class NewsEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        sentiment: str,

        confidence: float,

        headlines: list[dict],

    ) -> dict:

        score = 0

        reasons = []

        sentiment = (

            sentiment or "NEUTRAL"

        ).upper()

        confidence = max(

            0.0,

            min(

                confidence,

                1.0,

            ),

        )

        headline_count = len(

            headlines,

        )

        if sentiment == "VERY_POSITIVE":

            score = 10

            reasons.append(

                "Very positive news sentiment."

            )

        elif sentiment == "POSITIVE":

            score = 8

            reasons.append(

                "Positive news sentiment."

            )

        elif sentiment == "NEUTRAL":

            score = 3

            reasons.append(

                "Neutral news sentiment."

            )

        elif sentiment == "NEGATIVE":

            score = 1

            reasons.append(

                "Negative news sentiment."

            )

        else:

            score = 0

            reasons.append(

                "Very negative news sentiment."

            )

        if confidence >= 0.90:

            reasons.append(

                "Very high confidence news."

            )

        elif confidence >= 0.75:

            reasons.append(

                "High confidence news."

            )

        elif confidence >= 0.60:

            reasons.append(

                "Moderate confidence news."

            )

        else:

            reasons.append(

                "Low confidence news."

            )

        reasons.append(

            f"{headline_count} recent headlines available."

        )

        score = min(

            score,

            self.MAX_SCORE,

        )

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                confidence * 100,

            ),

            "sentiment": sentiment,

            "headline_count": headline_count,

            "reasons": reasons,

        }