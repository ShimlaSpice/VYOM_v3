"""
Confidence Engine.

Calculates overall confidence from all
intelligence modules.
"""

from __future__ import annotations


class ConfidenceEngine:

    WEIGHTS = {

        "technical": 35,

        "fundamental": 20,

        "news": 10,

        "sector": 10,

        "relative_strength": 10,

        "market": 10,

        "risk": 5,
    }

    def calculate(

        self,

        technical: float,

        fundamental: float,

        news: float,

        sector: float,

        relative_strength: float,

        market: float,

        risk: float,

    ) -> dict:

        score = (

            technical

            + fundamental

            + news

            + sector

            + relative_strength

            + market

            + risk

        )

        score = max(
            0,
            min(
                round(score),
                100,
            ),
        )

        if score >= 90:

            grade = "A+"

        elif score >= 80:

            grade = "A"

        elif score >= 70:

            grade = "B"

        elif score >= 60:

            grade = "C"

        else:

            grade = "D"

        return {

            "confidence": score,

            "grade": grade,

            "breakdown": {

                "technical": technical,

                "fundamental": fundamental,

                "news": news,

                "sector": sector,

                "relative_strength": relative_strength,

                "market": market,

                "risk": risk,

            },

        }