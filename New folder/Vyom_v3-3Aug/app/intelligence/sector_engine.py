"""
Sector Intelligence Engine.
"""

from __future__ import annotations


class SectorEngine:

    MAX_SCORE = 10

    STRONG_SECTORS = {

        "BANKING",

        "FINANCIAL SERVICES",

        "TECHNOLOGY",

        "INFORMATION TECHNOLOGY",

        "ENERGY",

        "HEALTHCARE",

        "PHARMACEUTICALS",

        "CAPITAL GOODS",

        "AUTOMOBILE",

        "AUTO",

        "FMCG",

    }

    GOOD_SECTORS = {

        "CHEMICALS",

        "INFRASTRUCTURE",

        "CONSUMER GOODS",

        "CEMENT",

        "METALS",

        "POWER",

        "TELECOM",

    }

    WEAK_SECTORS = {

        "REAL ESTATE",

        "MEDIA",

        "TEXTILE",

    }

    def evaluate(

        self,

        sector: str,

    ) -> dict:

        sector = (

            sector or "UNKNOWN"

        ).strip()

        sector_upper = sector.upper()

        score = 5

        reasons = []

        if sector_upper in self.STRONG_SECTORS:

            score = 10

            reasons.append(

                f"Very Strong Sector ({sector})"

            )

        elif sector_upper in self.GOOD_SECTORS:

            score = 8

            reasons.append(

                f"Strong Sector ({sector})"

            )

        elif sector_upper in self.WEAK_SECTORS:

            score = 2

            reasons.append(

                f"Weak Sector ({sector})"

            )

        else:

            score = 5

            reasons.append(

                f"Neutral Sector ({sector})"

            )

        return {

            "sector": sector,

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "reasons": reasons,

        }