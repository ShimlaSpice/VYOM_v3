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

from __future__ import annotations

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

        recommendations = []

        for candidate in scan_result.candidates:

            candles = self.provider.get_candles(

                symbol=candidate.symbol,

                interval="1d",

                limit=100,

            )

            if len(candles) < 50:

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

            recommendations.append(

                recommendation,

            )

        return self.top10.generate(

            recommendations,

            limit=filters.get(

                "top",

                10,

            ),

        )