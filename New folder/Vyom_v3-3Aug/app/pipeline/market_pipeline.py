"""
Complete Market Pipeline.

UI
 ↓
Scanner
 ↓
Recommendation Pipeline
 ↓
Top10
"""

from app.market.provider_manager import ProviderManager
from app.pipeline.recommendation_pipeline import RecommendationPipeline
from app.scanner.scanner import ScannerEngine
from app.top10 import Top10Engine


class MarketPipeline:

    def __init__(self):

        self.provider = ProviderManager()

        self.provider.connect()

        self.scanner = ScannerEngine(
            self.provider,
        )

        self.pipeline = RecommendationPipeline()

        self.top10 = Top10Engine()

    def run(
        self,
        filters: dict | None = None,
    ):

        if filters is None:

            filters = {
                "universe": "NIFTY50",
                "top": 10,
            }

        scan_result = self.scanner.scan(
            filters=filters,
        )

        candidates = scan_result.candidates

        if not candidates:
            return []

        symbols = [
            c.symbol
            for c in candidates
        ]

        self.provider.prefetch(
            symbols=symbols,
            period="6mo",
            interval="1d",
        )

        recommendations = []

        for candidate in candidates:

            print(f"[PIPELINE] {candidate.symbol}")

            try:

                candles = self.provider.get_candles(
                    symbol=candidate.symbol,
                    interval="1d",
                    limit=100,
                )

                if len(candles) < 50:
                    print(f"[SKIP] {candidate.symbol} (Not enough candles)")
                    continue

                fundamentals = self.provider.get_fundamentals(
                    candidate.symbol,
                ) or {}

                news = self.provider.get_news(
                    candidate.symbol,
                ) or {
                    "sentiment": "NEUTRAL",
                    "confidence": 0.50,
                    "headlines": [],
                }

                recommendation = self.pipeline.build(
                    candidate=candidate,
                    candles=candles,
                    fundamentals=fundamentals,
                    news=news,
                    sector=fundamentals.get(
                        "sector",
                        "Unknown",
                    ),
                )

                if recommendation is None:
                    print(f"[SKIP] {candidate.symbol} (No recommendation)")
                    continue

                print(f"[OK] {candidate.symbol}")

                recommendations.append(
                    recommendation,
                )

            except Exception:

                print(f"[FAILED] {candidate.symbol}")

                import traceback
                traceback.print_exc()

        recommendations.sort(
            key=lambda x: (
                getattr(x, "confidence", 0),
                getattr(x, "probability", 0),
            ),
            reverse=True,
        )

        print(f"\nGenerated {len(recommendations)} recommendations.\n")

        return self.top10.generate(
            recommendations,
            limit=filters.get(
                "top",
                10,
            ),
        )