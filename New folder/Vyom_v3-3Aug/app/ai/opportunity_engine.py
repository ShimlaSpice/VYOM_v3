"""
Opportunity Engine for VYOM.

Determines whether a stock is worth considering
among today's opportunities.
"""

from __future__ import annotations


class OpportunityEngine:

    def evaluate(

        self,

        probability: int,

        conviction: int,

        technical_score: int,

        catalyst_strength: int,

        risk_score: int,

    ) -> dict:

        score = (

            probability * 0.30

            + conviction * 0.30

            + technical_score * 2

            + catalyst_strength * 3

            + risk_score * 1

        )

        score = max(

            0,

            min(

                round(score),

                100,

            ),

        )

        if score >= 90:

            opportunity = "EXCEPTIONAL"

            priority = 1

        elif score >= 80:

            opportunity = "HIGH"

            priority = 2

        elif score >= 70:

            opportunity = "GOOD"

            priority = 3

        elif score >= 60:

            opportunity = "AVERAGE"

            priority = 4

        else:

            opportunity = "LOW"

            priority = 5

        return {

            "score": score,

            "opportunity": opportunity,

            "priority": priority,

        }