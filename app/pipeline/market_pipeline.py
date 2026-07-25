"""
Complete Market Pipeline.

Scanner
    ↓
Recommendation Pipeline
    ↓
Top 10 Engine
"""

from __future__ import annotations

from app.market import YahooFinanceProvider
from app.news.news_engine import NewsEngine
from app.scanner.scanner import ScannerEngine
from app.pipeline.recommendation_pipeline import (
    RecommendationPipeline,
)
from app.top10 import Top10Engine


class MarketPipeline:

    def __init__(self):

        self.provider = YahooFinanceProvider()

        self.news_engine = NewsEngine()

        self.scanner = ScannerEngine(
            self.provider,
        )

        self.pipeline = RecommendationPipeline()

        self.top10 = Top10Engine()

    def run(self):

        scan_result = self.scanner.scan()

        recommendations = []

        for candidate in scan_result.candidates:

            candles = self.provider.get_candles(

                symbol=candidate.symbol,

                interval="1d",

                limit=60,

            )

            if not candles:

                continue

            fundamentals = self.provider.get_fundamentals(
                candidate.symbol,
            )

            if not fundamentals:

                fundamentals = {}

            news = self.news_engine.analyze(
                candidate.symbol,
                limit=5,
            )

            sector = fundamentals.get(

                "sector",

                "Unknown",

            )

            recommendation = self.pipeline.build(

                candidate=candidate,

                candles=candles,

                fundamentals=fundamentals,

                news=news,

                sector=sector,

            )

            recommendations.append(
                recommendation
            )

        return self.top10.generate(
            recommendations
        )