"""
Live News Engine for VYOM.
"""

from __future__ import annotations

import feedparser


class NewsEngine:

    RSS_URL = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline"
    )

    POSITIVE_WORDS = {

        "gain",
        "gains",
        "growth",
        "profit",
        "profits",
        "buy",
        "bullish",
        "surge",
        "record",
        "strong",
        "upgrade",
        "upgrades",
        "beat",
        "beats",
        "expansion",
        "partnership",
        "contract",
        "order",
        "approval",
        "launch",

    }

    NEGATIVE_WORDS = {

        "fall",
        "falls",
        "loss",
        "losses",
        "weak",
        "fraud",
        "decline",
        "drop",
        "miss",
        "misses",
        "downgrade",
        "downgrades",
        "probe",
        "investigation",
        "penalty",
        "lawsuit",
        "default",
        "warning",

    }

    def analyze(

        self,

        symbol: str,

        limit: int = 5,

    ) -> dict:

        ticker = symbol.replace(

            ".NS",

            "",

        )

        url = (

            f"{self.RSS_URL}"

            f"?s={ticker}"

            "&region=US"

            "&lang=en-US"

        )

        try:

            feed = feedparser.parse(url)

        except Exception:

            return {

                "symbol": symbol,

                "sentiment": "NEUTRAL",

                "confidence": 0.50,

                "headlines": [],

            }

        headlines = []

        score = 0

        for entry in feed.entries[:limit]:

            title = getattr(

                entry,

                "title",

                "",

            )

            link = getattr(

                entry,

                "link",

                "",

            )

            headlines.append(

                {

                    "title": title,

                    "link": link,

                }

            )

            lower = title.lower()

            for word in self.POSITIVE_WORDS:

                if word in lower:

                    score += 1

            for word in self.NEGATIVE_WORDS:

                if word in lower:

                    score -= 1

        if score >= 3:

            sentiment = "VERY_POSITIVE"

            confidence = 0.95

        elif score > 0:

            sentiment = "POSITIVE"

            confidence = 0.80

        elif score <= -3:

            sentiment = "VERY_NEGATIVE"

            confidence = 0.95

        elif score < 0:

            sentiment = "NEGATIVE"

            confidence = 0.80

        else:

            sentiment = "NEUTRAL"

            confidence = 0.50

        return {

            "symbol": symbol,

            "sentiment": sentiment,

            "confidence": confidence,

            "headlines": headlines,

            "score": score,

        }