"""
Ranking Engine.
"""

from __future__ import annotations


class RankingEngine:

    def rank(
        self,
        recommendations: list,
    ):

        return sorted(

            recommendations,

            key=lambda x: (

                x.confidence,

                x.scores.get(
                    "technical",
                    0,
                ),

                x.scores.get(
                    "fundamental",
                    0,
                ),

                x.scores.get(
                    "news",
                    0,
                ),

            ),

            reverse=True,

        )