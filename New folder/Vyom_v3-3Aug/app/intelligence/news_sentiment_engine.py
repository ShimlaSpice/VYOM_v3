"""
News Sentiment Engine.

Calculates sentiment from news headlines.
"""

from __future__ import annotations


class NewsSentimentEngine:

    POSITIVE = {

        "profit",
        "profits",
        "growth",
        "record",
        "strong",
        "surge",
        "gain",
        "gains",
        "buy",
        "bullish",
        "expansion",
        "contract",
        "contracts",
        "upgrade",
        "upgrades",
        "beat",
        "beats",
        "approval",
        "launch",
        "orders",
        "order",
        "positive",

    }

    NEGATIVE = {

        "loss",
        "losses",
        "fall",
        "falls",
        "decline",
        "drop",
        "crash",
        "downgrade",
        "downgrades",
        "weak",
        "fraud",
        "penalty",
        "investigation",
        "probe",
        "default",
        "miss",
        "misses",
        "bearish",
        "negative",

    }

    def evaluate(

        self,

        headlines: list[dict],

    ) -> dict:

        positive = 0

        negative = 0

        reasons = []

        for headline in headlines:

            text = headline.get(

                "title",

                "",

            ).lower()

            positive += sum(

                word in text

                for word in self.POSITIVE

            )

            negative += sum(

                word in text

                for word in self.NEGATIVE

            )

        score = positive - negative

        if score >= 3:

            sentiment = "VERY_POSITIVE"

            confidence = 0.95

        elif score > 0:

            sentiment = "POSITIVE"

            confidence = min(

                0.90,

                0.65 + score * 0.05,

            )

        elif score <= -3:

            sentiment = "VERY_NEGATIVE"

            confidence = 0.95

        elif score < 0:

            sentiment = "NEGATIVE"

            confidence = min(

                0.90,

                0.65 + abs(score) * 0.05,

            )

        else:

            sentiment = "NEUTRAL"

            confidence = 0.50

        reasons.append(

            f"Positive keywords: {positive}"

        )

        reasons.append(

            f"Negative keywords: {negative}"

        )

        reasons.append(

            f"Headline score: {score}"

        )

        return {

            "sentiment": sentiment,

            "confidence": round(

                confidence,

                2,

            ),

            "score": score,

            "headlines": headlines,

            "reasons": reasons,

        }