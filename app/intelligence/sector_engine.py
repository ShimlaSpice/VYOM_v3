"""
Sector Intelligence Engine.
"""

from __future__ import annotations


class SectorEngine:

    SCORES = {

        "Financial Services": 10,

        "Banking": 10,

        "Technology": 10,

        "Information Technology": 10,

        "Energy": 9,

        "Oil & Gas": 9,

        "Capital Goods": 9,

        "Automobile": 8,

        "Healthcare": 8,

        "Pharmaceuticals": 8,

        "FMCG": 8,

        "Consumer Defensive": 8,

        "Consumer Cyclical": 7,

        "Telecommunication": 7,

        "Telecom": 7,

        "Infrastructure": 7,

        "Chemicals": 7,

        "Metals": 6,

        "Mining": 6,

        "Power": 6,

        "Utilities": 6,

        "Construction": 5,

        "Real Estate": 3,

        "Media": 2,

        "Textile": 2,

    }

    def evaluate(

        self,

        sector: str,

    ) -> dict:

        sector = (sector or "Unknown").strip()

        score = self.SCORES.get(

            sector,

            5,

        )

        reasons = []

        if score >= 9:

            reasons.append(

                f"Very Strong Sector ({sector})"

            )

        elif score >= 7:

            reasons.append(

                f"Strong Sector ({sector})"

            )

        elif score >= 5:

            reasons.append(

                f"Neutral Sector ({sector})"

            )

        else:

            reasons.append(

                f"Weak Sector ({sector})"

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