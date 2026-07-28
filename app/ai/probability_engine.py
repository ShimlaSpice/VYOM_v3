"""
Probability Engine for VYOM.

Estimates the probability of a successful trade.
"""

from __future__ import annotations


class ProbabilityEngine:

    MAX_SCORE = 100

    def calculate(

        self,

        technical: int,

        fundamental: int,

        news: int,

        sector: int,

        risk: int,

        confidence: int,

    ) -> dict:

        score = (

            (technical * 0.35)

            + (fundamental * 0.20)

            + (news * 0.10)

            + (sector * 0.10)

            + (risk * 0.10)

            + (confidence * 0.15)

        )

        probability = max(

            0,

            min(

                round(score),

                self.MAX_SCORE,

            ),

        )

        if probability >= 90:

            verdict = "VERY HIGH"

        elif probability >= 80:

            verdict = "HIGH"

        elif probability >= 70:

            verdict = "GOOD"

        elif probability >= 60:

            verdict = "MODERATE"

        else:

            verdict = "LOW"

        return {

            "probability": probability,

            "verdict": verdict,

        }