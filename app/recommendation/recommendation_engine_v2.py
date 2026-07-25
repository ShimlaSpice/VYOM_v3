"""
Recommendation Engine V2.

Combines all intelligence engines into one final recommendation.
"""

from __future__ import annotations

from app.recommendation.recommendation_model import Recommendation


class RecommendationEngineV2:

    def generate(

        self,

        symbol: str,

        technical: dict,

        fundamental: dict,

        news: dict,

        sector: dict,

        risk: dict,

        confidence: dict,

        trade_setup: dict,

        trade_type: dict,

    ) -> Recommendation:

        reasons = []

        reasons.extend(technical["reasons"])
        reasons.extend(fundamental["reasons"])
        reasons.extend(news["reasons"])
        reasons.extend(sector["reasons"])
        reasons.extend(risk["reasons"])

        confidence_score = confidence["confidence"]

        category = trade_type["category"]

        if category == "POSITIONAL":

            recommendation = (
                "STRONG BUY"
                if confidence_score >= 90
                else "BUY"
            )

        elif category == "SWING":

            recommendation = (
                "BUY"
                if confidence_score >= 75
                else "WATCH"
            )

        elif category == "INTRADAY":

            recommendation = (
                "BUY"
                if confidence_score >= 70
                else "WATCH"
            )

        elif category == "WATCH":

            recommendation = "WATCH"

        else:

            recommendation = "AVOID"

        scores = {

            "technical": technical["score"],

            "fundamental": fundamental["score"],

            "news": news["score"],

            "sector": sector["score"],

            "risk": risk["score"],

            "confidence": confidence_score,

        }

        return Recommendation(

            symbol=symbol,

            recommendation=recommendation,

            category=category,

            confidence=confidence_score,

            entry=trade_setup["entry"],

            stop_loss=trade_setup["stop_loss"],

            target1=trade_setup["target1"],

            target2=trade_setup["target2"],

            risk_reward=trade_setup["risk_reward"],

            risk_level=risk["risk_level"],

            reasons=reasons,

            scores=scores,

        )