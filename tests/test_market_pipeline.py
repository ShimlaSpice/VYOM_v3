from app.pipeline import MarketPipeline
from app.recommendation import RecommendationFormatter

pipeline = MarketPipeline()

recommendations = pipeline.run()

formatter = RecommendationFormatter()

print()

print("=" * 80)
print("VYOM DAILY RECOMMENDATIONS")
print("=" * 80)
print()

for i, recommendation in enumerate(recommendations, start=1):

    print(f"RANK #{i}")

    print(
        formatter.format(
            recommendation
        )
    )

    print()