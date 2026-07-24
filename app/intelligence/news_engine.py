"""
News Intelligence Engine.
"""

from __future__ import annotations


class NewsEngine:

    def evaluate(
        self,
        sentiment: str,
        confidence: float,
        headlines: list[dict],
    ) -> dict:

        score = 0

        reasons = []

        sentiment = sentiment.upper()

        # -------------------------------------
        # Sentiment
        # -------------------------------------

        if sentiment == "POSITIVE":

            score += 6

            reasons.append(
                "Positive news sentiment."
            )

        elif sentiment == "NEUTRAL":

            score += 3

            reasons.append(
                "Neutral news sentiment."
            )

        else:

            reasons.append(
                "Negative news sentiment."
            )

        # -------------------------------------
        # Confidence
        # -------------------------------------

        if confidence >= 0.80:

            score += 2

            reasons.append(
                "High confidence news."
            )

        elif confidence >= 0.60:

            score += 1

            reasons.append(
                "Moderately reliable news."
            )

        # -------------------------------------
        # Headline Count
        # -------------------------------------

        count = len(headlines)

        if count >= 5:

            score += 2

            reasons.append(
                f"{count} relevant headlines found."
            )

        elif count > 0:

            score += 1

            reasons.append(
                f"{count} recent headlines available."
            )

        score = min(score, 10)

        return {

            "score": score,

            "max_score": 10,

            "confidence": round(
                (score / 10) * 100
            ),

            "reasons": reasons,

        }