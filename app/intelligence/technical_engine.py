"""
Technical Intelligence Engine.
"""

from __future__ import annotations


class TechnicalEngine:

    MAX_SCORE = 35

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

        total = 0

        reasons = []

        if sma:

            total += 5

            reasons.append(

                "Price above SMA20"

            )

        if ema:

            total += 5

            reasons.append(

                "Price above EMA20"

            )

        if 45 <= rsi <= 65:

            total += 5

            reasons.append(

                f"Healthy RSI ({rsi:.2f})"

            )

        elif rsi > 65:

            total += 3

            reasons.append(

                f"Strong RSI ({rsi:.2f})"

            )

        if macd > 0:

            total += 5

            reasons.append(

                "Positive MACD"

            )

        if breakout:

            total += 8

            reasons.append(

                "20-Day Breakout"

            )

        if volume:

            total += 7

            reasons.append(

                "High Volume Confirmation"

            )

        total = min(

            total,

            self.MAX_SCORE,

        )

        confidence = round(

            (total / self.MAX_SCORE) * 100

        )

        return {

            "score": total,

            "max_score": self.MAX_SCORE,

            "confidence": confidence,

            "reasons": reasons,

        }