"""
Rejection Engine for VYOM.

Explains why a stock was rejected.
"""

from __future__ import annotations


class RejectionEngine:

    def evaluate(

        self,

        technical: dict,

        fundamental: dict,

        news: dict,

        sector: dict,

        risk: dict,

        probability: int,

    ) -> dict:

        reasons: list[str] = []

        if technical.get(

            "score",

            0,

        ) < 20:

            reasons.append(

                "Weak Technical Setup"

            )

        if fundamental.get(

            "score",

            0,

        ) < 10:

            reasons.append(

                "Weak Fundamentals"

            )

        if news.get(

            "sentiment",

            "NEUTRAL",

        ) == "NEGATIVE":

            reasons.append(

                "Negative News Sentiment"

            )

        if sector.get(

            "score",

            0,

        ) < 5:

            reasons.append(

                "Weak Sector Momentum"

            )

        if risk.get(

            "risk_level",

            "HIGH",

        ) == "HIGH":

            reasons.append(

                "High Trading Risk"

            )

        if probability < 60:

            reasons.append(

                "Low Probability Setup"

            )

        if not reasons:

            status = "ACCEPTED"

        else:

            status = "REJECTED"

        return {

            "status": status,

            "count": len(

                reasons,

            ),

            "reasons": reasons,

        }