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
from app.scanner.scanner import ScannerEngine
from app.pipeline.recommendation_pipeline import (
    RecommendationPipeline,
)
from app.top10 import Top10Engine


class MarketPipeline:

    def __init__(self):

        self.provider = YahooFinanceProvider()

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

            # --------------------------------------------------
            # Temporary placeholders
            # Replace with real engines later
            # --------------------------------------------------

            fundamentals = {

                "pe": 22,

                "eps": 65,

                "roe": 18,

                "debt_to_equity": 45,

                "market_cap": 1800000000000,

            }

            news = {

                "sentiment": "POSITIVE",

                "confidence": 0.90,

                "headlines": [

                    {

                        "title":
                        "Positive Quarterly Results"

                    },

                    {

                        "title":
                        "Broker Upgrade"

                    },

                ],

            }

            sector = "Financial Services"

            recommendation = self.pipeline.build(

                candidate=candidate,

                candles=candles,

                fundamentals=fundamentals,

                news=news,

                sector=sector,

            )
            print(
                recommendation.symbol,
                recommendation.entry,
                recommendation.stop_loss,
                recommendation.target1,
                recommendation.target2,
            )


            recommendations.append(
                recommendation
            )

        return self.top10.generate(
            recommendations
        )