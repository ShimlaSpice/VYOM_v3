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

    ):

        ranked = self.ranker.rank(
            recommendations
        )

        return ranked[:limit]