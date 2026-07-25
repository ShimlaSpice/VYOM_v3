"""
Top 10 Engine.
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

    ) -> list:

        if not recommendations:

            return []

        ranked = self.ranker.rank(

            recommendations,

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