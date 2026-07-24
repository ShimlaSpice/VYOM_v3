"""
Live News Engine for VYOM.
"""

from __future__ import annotations

import feedparser


class NewsEngine:
    """
    Fetches latest Yahoo Finance news headlines.
    """

    RSS_URL = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline"
    )

    def analyze(
        self,
        symbol: str,
        limit: int = 5,
    ) -> dict:

        ticker = symbol.replace(".NS", "")

        url = (
            f"{self.RSS_URL}"
            f"?s={ticker}"
            f"&region=US"
            f"&lang=en-US"
        )

        feed = feedparser.parse(url)

        headlines = []

        for entry in feed.entries[:limit]:

            headlines.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                }
            )

        sentiment = "NEUTRAL"

        confidence = 0.50

        positive_words = [
            "gain",
            "growth",
            "profit",
            "buy",
            "surge",
            "record",
            "strong",
            "upgrade",
            "beat",
        ]

        negative_words = [
            "fall",
            "loss",
            "downgrade",
            "weak",
            "fraud",
            "decline",
            "drop",
            "miss",
        ]

        score = 0

        for item in headlines:

            title = item["title"].lower()

            for word in positive_words:
                if word in title:
                    score += 1

            for word in negative_words:
                if word in title:
                    score -= 1

        if score > 0:
            sentiment = "POSITIVE"
            confidence = 0.75

        elif score < 0:
            sentiment = "NEGATIVE"
            confidence = 0.75

        return {
            "symbol": symbol,
            "sentiment": sentiment,
            "confidence": confidence,
            "headlines": headlines,
        }