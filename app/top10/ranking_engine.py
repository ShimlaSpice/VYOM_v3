"""
Top 10 Ranking Engine.
"""

from __future__ import annotations


class RankingEngine:

    def rank(

        self,

        recommendations: list,

    ) -> list:

        return sorted(

            recommendations,

            key=lambda recommendation: (

                recommendation.confidence,

                recommendation.scores.get(

                    "technical",

                    0,

                ),

                recommendation.scores.get(

                    "fundamental",

                    0,

                ),

                recommendation.scores.get(

                    "news",

                    0,

                ),

                recommendation.scores.get(

                    "sector",

                    0,

                ),

                recommendation.scores.get(

                    "risk",

                    0,

                ),

                recommendation.symbol,

            ),

            reverse=True,

        )