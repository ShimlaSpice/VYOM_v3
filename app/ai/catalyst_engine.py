"""
Catalyst Engine for VYOM.

Identifies the key reasons behind a trading opportunity.
"""

from __future__ import annotations


class CatalystEngine:

    def analyze(

        self,

        technical: dict,

        fundamental: dict,

        news: dict,

        sector: dict,

    ) -> dict:

        catalysts: list[str] = []

        strength = 0

        # ----------------------------------------
        # Technical
        # ----------------------------------------

        if technical.get("score", 0) >= 30:

            catalysts.append(

                "Strong Technical Structure"

            )

            strength += 3

        elif technical.get("score", 0) >= 20:

            catalysts.append(

                "Improving Technical Momentum"

            )

            strength += 2

        # ----------------------------------------
        # Fundamentals
        # ----------------------------------------

        if fundamental.get("score", 0) >= 15:

            catalysts.append(

                "Strong Company Fundamentals"

            )

            strength += 2

        # ----------------------------------------
        # News
        # ----------------------------------------

        if news.get(

            "sentiment",

            "",

        ) == "POSITIVE":

            catalysts.append(

                "Positive News Flow"

            )

            strength += 2

        # ----------------------------------------
        # Sector
        # ----------------------------------------

        if sector.get("score", 0) >= 8:

            catalysts.append(

                "Sector Outperforming Market"

            )

            strength += 2

        # ----------------------------------------
        # Overall Strength
        # ----------------------------------------

        if strength >= 8:

            rating = "VERY STRONG"

        elif strength >= 6:

            rating = "STRONG"

        elif strength >= 4:

            rating = "MODERATE"

        elif strength >= 2:

            rating = "WEAK"

        else:

            rating = "NONE"

        return {

            "strength": strength,

            "rating": rating,

            "catalysts": catalysts,

        }