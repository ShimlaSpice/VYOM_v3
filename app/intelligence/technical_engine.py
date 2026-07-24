"""
Technical Intelligence Engine.
"""

from __future__ import annotations


class TechnicalEngine:

    def evaluate(
        self,
        score: int,
        rsi: float,
        macd: float,
        sma: bool,
        ema: bool,
        breakout: bool,
        volume: bool,
    ) -> dict:

        reasons = []

        technical_score = 0

        if sma:
            technical_score += 5
            reasons.append("Price above SMA20")

        if ema:
            technical_score += 5
            reasons.append("Price above EMA20")

        if 45 <= rsi <= 65:
            technical_score += 5
            reasons.append(f"Healthy RSI ({rsi:.2f})")

        if macd > 0:
            technical_score += 5
            reasons.append("Positive MACD")

        if breakout:
            technical_score += 10
            reasons.append("Breakout confirmed")

        if volume:
            technical_score += 5
            reasons.append("Volume confirmation")

        technical_score += min(score, 35)

        technical_score = min(
            technical_score,
            35,
        )

        confidence = round(
            (technical_score / 35) * 100,
        )

        return {

            "score": technical_score,

            "max_score": 35,

            "confidence": confidence,

            "reasons": reasons,

        }