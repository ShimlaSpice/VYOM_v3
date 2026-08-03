"""
Corporate Action Intelligence Engine.

Evaluates the impact of corporate actions on
investment decisions.
"""

from __future__ import annotations


class CorporateActionEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        bonus: bool = False,

        split: bool = False,

        dividend: bool = False,

        buyback: bool = False,

        rights_issue: bool = False,

        merger: bool = False,

    ) -> dict:

        score = 5

        reasons = []

        # ----------------------------------------
        # Bonus Issue
        # ----------------------------------------

        if bonus:

            score += 2

            reasons.append(

                "Bonus Issue Announced"

            )

        # ----------------------------------------
        # Stock Split
        # ----------------------------------------

        if split:

            score += 1

            reasons.append(

                "Stock Split Announced"

            )

        # ----------------------------------------
        # Dividend
        # ----------------------------------------

        if dividend:

            score += 1

            reasons.append(

                "Dividend Declared"

            )

        # ----------------------------------------
        # Buyback
        # ----------------------------------------

        if buyback:

            score += 2

            reasons.append(

                "Share Buyback Announced"

            )

        # ----------------------------------------
        # Rights Issue
        # ----------------------------------------

        if rights_issue:

            score -= 2

            reasons.append(

                "Rights Issue Announced"

            )

        # ----------------------------------------
        # Merger / Acquisition
        # ----------------------------------------

        if merger:

            score += 1

            reasons.append(

                "Merger / Acquisition News"

            )

        score = max(

            0,

            min(

                score,

                self.MAX_SCORE,

            ),

        )

        if score >= 8:

            outlook = "POSITIVE"

        elif score >= 5:

            outlook = "NEUTRAL"

        else:

            outlook = "NEGATIVE"

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "outlook": outlook,

            "reasons": reasons,

        }