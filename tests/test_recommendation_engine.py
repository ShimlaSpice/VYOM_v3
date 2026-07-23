from app.ai.recommendation_engine import RecommendationEngine
from app.scanner.models import ScanCandidate

candidate = ScanCandidate(
    symbol="ICICIBANK.NS",
    score=70,
    reasons=[
        "Price above SMA20",
        "MACD Positive",
        "Healthy RSI",
    ],
)

engine = RecommendationEngine()

recommendation = engine.recommend(
    candidate,
    market={"trend": "BULLISH"},
    sector="BANK",
    news={"sentiment": "NEUTRAL"},
)

print()

print("=" * 60)

for key, value in recommendation.items():
    print(f"{key:12}: {value}")