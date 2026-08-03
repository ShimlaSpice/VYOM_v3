"""
Top 10 Ranking Engine.
"""

from __future__ import annotations

from typing import Any


class RankingEngine:

    def rank(

        self,

        recommendations: list[Any],

    ) -> list[Any]:

        if not recommendations:

            return []

        return sorted(

            recommendations,

            key=self._sort_key,

            reverse=True,

        )

    @staticmethod
    def _sort_key(

        recommendation: Any,

    ):

        scores = getattr(

            recommendation,

            "scores",

            {},

        )

        return (

            getattr(

                recommendation,

                "confidence",

                0,

            ),

            getattr(

                recommendation,

                "probability",

                0,

            ),

            scores.get(

                "technical",

                0,

            ),

            scores.get(

                "fundamental",

                0,

            ),

            scores.get(

                "news",

                0,

            ),

            scores.get(

                "sector",

                0,

            ),

            scores.get(

                "risk",

                0,

            ),

            getattr(

                recommendation,

                "symbol",

                "",

            ),

        )