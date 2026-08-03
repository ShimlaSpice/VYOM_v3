"""
Top Recommendation Engine.

Filters, ranks, sorts, and deduplicates recommendations down to a
final top-N list, returned as the boundary-facing RankedStock model.
"""

from __future__ import annotations

from typing import Any

from app.top10.models import RankedStock
from app.top10.ranking_engine import RankingEngine

_ACTIONABLE_DECISIONS = ("STRONG BUY", "BUY", "WATCH")


class Top10Engine:

    def __init__(self) -> None:
        self.ranker = RankingEngine()

    def generate(

        self,

        recommendations: list[Any],

        limit: int = 10,

        sort_by: str = "Confidence",

    ) -> list[RankedStock]:

        if not recommendations:

            return []

        ranked = self.ranker.rank(

            [

                r

                for r in recommendations

                if r.recommendation

                in _ACTIONABLE_DECISIONS

            ]

        )

        if not ranked:

            return []

        sort_key = sort_by.lower()

        key_map = {

            "confidence": lambda r: (

                r.confidence,

                getattr(

                    r,

                    "probability",

                    0,

                ),

                r.scores.get(

                    "technical",

                    0,

                ),

            ),

            "probability": lambda r: (

                getattr(

                    r,

                    "probability",

                    0,

                ),

                r.confidence,

            ),

            "score": lambda r: (

                r.scores.get(

                    "technical",

                    0,

                ),

                r.confidence,

            ),

            "price": lambda r: (

                getattr(

                    r,

                    "entry",

                    0,

                ),

            ),

        }

        ranked.sort(

            key=key_map.get(

                sort_key,

                key_map["confidence"],

            ),

            reverse=sort_key != "price",

        )

        seen = set()

        result = []

        append = result.append

        add = seen.add

        from_recommendation = RankedStock.from_recommendation

        for recommendation in ranked:

            symbol = recommendation.symbol

            if symbol in seen:

                continue

            add(symbol)

            append(

                from_recommendation(

                    recommendation,

                )

            )

            if len(result) >= limit:

                break

        return result