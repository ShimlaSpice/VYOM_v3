"""
Top Recommendation Engine.
"""

from __future__ import annotations

from app.top10.ranking_engine import RankingEngine


class Top10Engine:

    def __init__(self):

        self.ranker = RankingEngine()

    def generate(

        self,

        recommendations: list,

        limit: int = 10,

        sort_by: str = "Confidence",

    ) -> list:

        if not recommendations:

            return []

        recommendations = [

            recommendation

            for recommendation in recommendations

            if recommendation.recommendation

            in (

                "STRONG BUY",

                "BUY",

                "WATCH",

            )

        ]

        if not recommendations:

            return []

        ranked = self.ranker.rank(

            recommendations,

        )

        if sort_by.lower() == "score":

            ranked.sort(

                key=lambda x: x.scores.get(

                    "technical",

                    0,

                ),

                reverse=True,

            )

        elif sort_by.lower() == "probability":

            ranked.sort(

                key=lambda x: x.probability,

                reverse=True,

            )

        elif sort_by.lower() == "price":

            ranked.sort(

                key=lambda x: x.entry,

            )

        else:

            ranked.sort(

                key=lambda x: x.confidence,

                reverse=True,

            )

        final = []

        seen = set()

        for recommendation in ranked:

            if recommendation.symbol in seen:

                continue

            seen.add(

                recommendation.symbol,

            )

            final.append(

                recommendation,

            )

            if len(final) >= limit:

                break

        return final