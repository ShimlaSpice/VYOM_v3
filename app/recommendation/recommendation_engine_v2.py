"""
Recommendation Engine V2.
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

        probability: dict | None = None,

        conviction: dict | None = None,

        market_data: dict | None = None,

        fundamentals_data: dict | None = None,

    ) -> Recommendation:

        reasons: list[str] = []
        reasons.extend(technical.get("reasons", []))
        reasons.extend(fundamental.get("reasons", []))
        reasons.extend(news.get("reasons", []))
        reasons.extend(sector.get("reasons", []))
        reasons.extend(risk.get("reasons", []))
        reasons.extend(trade_type.get("reasons", []))

        confidence_score = int(confidence.get("confidence", 0))
        category = trade_type.get("category", "WATCH")

        if category == "POSITIONAL":

            recommendation = "STRONG BUY"

        elif category in ("SWING", "INTRADAY"):

            recommendation = "BUY"

        elif category == "WATCH":

            recommendation = "WATCH"

        else:

            recommendation = "AVOID"

        probability_value = 0

        conviction_value = "UNKNOWN"

        if probability:

            probability_value = probability.get(

                "probability",

                0,

            )

        if conviction:

            conviction_value = conviction.get(

                "level",

                conviction.get(

                    "action",

                    "UNKNOWN",

                ),

            )

        if market_data is None:

            market_data = {}

        if fundamentals_data is None:

            fundamentals_data = {}

        ai_summary = (
            f"{recommendation} | "
            f"Confidence {confidence_score}% | "
            f"Risk {risk.get('risk_level', 'MEDIUM')} | "
            f"{len(reasons)} Positive Signals"
        )

        scores = {
            "technical": technical.get("score", 0),
            "fundamental": fundamental.get("score", 0),
            "news": news.get("score", 0),
            "sector": sector.get("score", 0),
            "risk": risk.get("score", 0),
            "confidence": confidence_score,
        }

        return Recommendation(

            symbol=symbol,

            recommendation=recommendation,

            category=category,

            confidence=confidence_score,

            probability=probability_value,

            conviction=conviction_value,

            open=market_data.get(

                "open",

                0,

            ),

            high=market_data.get(

                "high",

                0,

            ),

            low=market_data.get(

                "low",

                0,

            ),

            close=market_data.get(

                "close",

                0,

            ),

            previous_close=market_data.get(

                "previous_close",

                0,

            ),

            change=market_data.get(

                "change",

                0,

            ),

            change_percent=market_data.get(

                "change_percent",

                0,

            ),

            volume=market_data.get(

                "volume",

                0,

            ),

            entry=trade_setup.get("entry", 0.0),

            stop_loss=trade_setup.get("stop_loss", 0.0),

            target1=trade_setup.get("target1", 0.0),

            target2=trade_setup.get("target2", 0.0),

            exit_price=trade_setup.get("target2", 0.0),

            risk_reward=trade_setup.get("risk_reward", 0.0),

            risk_level=risk.get("risk_level", "MEDIUM"),

            atr=risk.get(

                "atr",

                0,

            ),

            volatility=risk.get(

                "volatility",

                0,

            ),

            sector=fundamentals_data.get(

                "sector",

                "",

            ),

            industry=fundamentals_data.get(

                "industry",

                "",

            ),

            market_cap=fundamentals_data.get(

                "market_cap",

                0,

            ),

            pe=fundamentals_data.get(

                "pe",

                0,

            ),

            eps=fundamentals_data.get(

                "eps",

                0,

            ),

            roe=fundamentals_data.get(

                "roe",

                0,

            ),

            debt_to_equity=fundamentals_data.get(

                "debt_to_equity",

                0,

            ),

            reasons=reasons,

            ai_summary=ai_summary,

            scores=scores,

        )