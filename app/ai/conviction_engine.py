"""
Conviction Engine for VYOM.

Determines how strongly Jarvis believes
in a trading opportunity.
"""

from __future__ import annotations


class ConvictionEngine:

    def evaluate(

        self,

        probability: int,

        confidence: int,

        technical_score: int,

        risk_score: int,

    ) -> dict:

        score = (

            probability * 0.40

            + confidence * 0.30

            + technical_score * 2

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

            conviction = "EXTREME"

            action = "STRONG BUY"

        elif score >= 80:

            conviction = "HIGH"

            action = "BUY"

        elif score >= 70:

            conviction = "GOOD"

            action = "WATCH"

        elif score >= 60:

            conviction = "LOW"

            action = "WAIT"

        else:

            conviction = "VERY LOW"

            action = "AVOID"

        return {

            "score": score,

            "conviction": conviction,

            "action": action,

        }