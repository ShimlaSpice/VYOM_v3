"""
End-to-End Test for VYOM Market Pipeline.
"""

from __future__ import annotations

from app.pipeline import MarketPipeline
from app.recommendation.recommendation_formatter import (
    RecommendationFormatter,
)


def main():

    pipeline = MarketPipeline()

    formatter = RecommendationFormatter()

    recommendations = pipeline.run()

    print()

    print("=" * 80)

    print("VYOM DAILY RECOMMENDATIONS")

    print("=" * 80)

    if not recommendations:

        print()

        print("No recommendations generated.")

        return

    for rank, recommendation in enumerate(

        recommendations,

        start=1,

    ):

        print()

        print(f"RANK #{rank}")

        print(

            formatter.format(

                recommendation,

            )

        )


if __name__ == "__main__":

    main()