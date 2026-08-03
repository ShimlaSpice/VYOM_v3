"""
Recommendation Engine.
"""

from __future__ import annotations


class RecommendationEngine:

    def recommend(
        self,
        candidate,
        market,
        sector,
        news,
    ) -> dict:

        confidence = candidate.score

        if market["trend"] == "BULLISH":
            confidence += 10

        elif market["trend"] == "BEARISH":
            confidence -= 10

        if news["sentiment"] == "POSITIVE":
            confidence += 10

        elif news["sentiment"] == "NEGATIVE":
            confidence -= 15

        confidence = max(0, min(100, confidence))

        action = "HOLD"

        if confidence >= 80:
            action = "BUY"

        elif confidence >= 60:
            action = "WATCH"

        return {
            "symbol": candidate.symbol,
            "action": action,
            "confidence": confidence,
            "score": candidate.score,
            "market": market["trend"],
            "sector": sector,
            "news": news["sentiment"],
            "reasons": candidate.reasons,
        }