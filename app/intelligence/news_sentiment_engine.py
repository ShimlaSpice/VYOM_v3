"""
News Sentiment Engine.

Calculates sentiment from news headlines.
"""

from __future__ import annotations


class NewsSentimentEngine:

    POSITIVE = {

        "profit",
        "growth",
        "record",
        "strong",
        "surge",
        "gain",
        "buy",
        "bullish",
        "expansion",
        "contract",
        "upgrade",
        "beat",
        "highest",
        "positive",

    }

    NEGATIVE = {

        "loss",
        "fall",
        "decline",
        "downgrade",
        "weak",
        "fraud",
        "crash",
        "drop",
        "bearish",
        "penalty",
        "investigation",
        "miss",
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

            for word in self.POSITIVE:

                if word in text:

                    positive += 1

            for word in self.NEGATIVE:

                if word in text:

                    negative += 1

        if positive > negative:

            sentiment = "POSITIVE"

            confidence = min(
                0.95,
                0.60 + (positive * 0.05),
            )

        elif negative > positive:

            sentiment = "NEGATIVE"

            confidence = min(
                0.95,
                0.60 + (negative * 0.05),
            )

        else:

            sentiment = "NEUTRAL"

            confidence = 0.50

        reasons.append(

            f"{positive} Positive Keywords"

        )

        reasons.append(

            f"{negative} Negative Keywords"

        )

        return {

            "sentiment": sentiment,

            "confidence": round(
                confidence,
                2,
            ),

            "headlines": headlines,

            "reasons": reasons,

        }