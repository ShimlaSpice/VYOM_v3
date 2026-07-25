"""
Confidence Engine.
"""

from __future__ import annotations

import math


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

    @staticmethod
    def _safe(

        value,

    ) -> float:

        if value is None:

            return 0.0

        try:

            value = float(value)

        except Exception:

            return 0.0

        if math.isnan(value):

            return 0.0

        if math.isinf(value):

            return 0.0

        return value

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

        technical = self._safe(

            technical,

        )

        fundamental = self._safe(

            fundamental,

        )

        news = self._safe(

            news,

        )

        sector = self._safe(

            sector,

        )

        relative_strength = self._safe(

            relative_strength,

        )

        market = self._safe(

            market,

        )

        risk = self._safe(

            risk,

        )

        weighted_score = (

            (technical / 35) * self.WEIGHTS["technical"]

            + (fundamental / 20) * self.WEIGHTS["fundamental"]

            + (news / 10) * self.WEIGHTS["news"]

            + (sector / 10) * self.WEIGHTS["sector"]

            + (relative_strength / 10) * self.WEIGHTS["relative_strength"]

            + (market / 10) * self.WEIGHTS["market"]

            + (risk / 10) * self.WEIGHTS["risk"]

        )

        score = max(

            0,

            min(

                round(

                    weighted_score,

                ),

                100,

            ),

        )

        if score >= 90:

            grade = "A+"

        elif score >= 80:

            grade = "A"

        elif score >= 70:

            grade = "B+"

        elif score >= 60:

            grade = "B"

        elif score >= 50:

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