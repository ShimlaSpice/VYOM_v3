"""
Sector Intelligence Engine.
"""

from __future__ import annotations


class SectorEngine:

    STRONG_SECTORS = {

        "Financial Services",
        "Technology",
        "Banking",
        "Energy",
        "Healthcare",
        "Pharmaceuticals",
        "Capital Goods",
        "Automobile",

    }

    WEAK_SECTORS = {

        "Real Estate",
        "Media",
        "Textile",

    }

    def evaluate(
        self,
        sector: str,
    ) -> dict:

        score = 0

        reasons = []

        sector = sector.strip()

        # -------------------------------------
        # Strong Sector
        # -------------------------------------

        if sector in self.STRONG_SECTORS:

            score = 10

            reasons.append(
                f"Strong Sector ({sector})"
            )

        # -------------------------------------
        # Weak Sector
        # -------------------------------------

        elif sector in self.WEAK_SECTORS:

            score = 2

            reasons.append(
                f"Weak Sector ({sector})"
            )

        # -------------------------------------
        # Neutral Sector
        # -------------------------------------

        else:

            score = 5

            reasons.append(
                f"Neutral Sector ({sector})"
            )

        confidence = round(
            (score / 10) * 100
        )

        return {

            "sector": sector,

            "score": score,

            "max_score": 10,

            "confidence": confidence,

            "reasons": reasons,

        }