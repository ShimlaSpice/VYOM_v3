"""
Recommendation Pipeline for VYOM.

Converts ScanCandidate -> Recommendation.
"""

from __future__ import annotations

from app.intelligence import (
    IntelligenceEngine,
    MarketTrendEngine,
    NewsSentimentEngine,
)

from app.recommendation import RecommendationEngineV2

from app.trade_intelligence import (
    ATREngine,
    SetupGenerator,
    TradeClassifier,
)


class RecommendationPipeline:

    def __init__(self):

        self.atr_engine = ATREngine()

        self.trade_classifier = TradeClassifier()

        self.intelligence = IntelligenceEngine()

        self.recommendation = RecommendationEngineV2()

        self.market_trend = MarketTrendEngine()

        self.news_sentiment = NewsSentimentEngine()

        self.setup_generator = SetupGenerator()

    def build(

        self,

        candidate,

        candles,

        fundamentals: dict,

        news: dict,

        sector: str,

    ):

        closes = [

            candle["close"]

            for candle in candles

        ]

        highs = [

            candle["high"]

            for candle in candles

        ]

        lows = [

            candle["low"]

            for candle in candles

        ]

        volumes = [

            candle["volume"]

            for candle in candles

        ]

        atr_summary = self.atr_engine.summary(

            highs,

            lows,

            closes,

        )

        candidate.atr = atr_summary["atr"]

        candidate.pe = fundamentals.get(

            "pe",

        )

        candidate.eps = fundamentals.get(

            "eps",

        )

        candidate.roe = fundamentals.get(

            "roe",

        )

        candidate.debt_to_equity = fundamentals.get(

            "debt_to_equity",

        )

        candidate.market_cap = fundamentals.get(

            "market_cap",

            0,

        )

        candidate.sector = sector

        candidate.industry = fundamentals.get(

            "industry",

            "",

        )

        market = self.market_trend.evaluate(

            closes,

        )

        news_analysis = self.news_sentiment.evaluate(

            news.get(

                "headlines",

                [],

            )

        )

        trade = self.trade_classifier.classify(

            score=candidate.score,

            atr_percent=atr_summary["atr_percent"],

            trend=market["trend"],

            sentiment=news_analysis["sentiment"],

        )

        setup = self.setup_generator.generate(

            highs,

            lows,

            closes,

            trade["category"],

        )

        intelligence = self.intelligence.analyze(

            technical_input={

                "score": candidate.score,

                "rsi": candidate.rsi,

                "macd": candidate.macd,

                "sma": candidate.price > candidate.sma20,

                "ema": candidate.price > candidate.ema20,

                "breakout": candidate.breakout,

                "volume": candidate.volume > candidate.average_volume * 1.5,

            },

            fundamental_input={

                "pe": candidate.pe,

                "eps": candidate.eps,

                "roe": candidate.roe,

                "debt_to_equity": candidate.debt_to_equity,

                "market_cap": candidate.market_cap,

            },

            news_input={

                "sentiment": news_analysis["sentiment"],

                "confidence": news_analysis["confidence"],

                "headlines": news_analysis["headlines"],

            },

            sector_input={

                "sector": candidate.sector,

            },

            risk_input={

                "atr_percent": atr_summary["atr_percent"],

                "volatility": atr_summary["volatility"],

                "risk_reward": setup["risk_reward"],

            },

            relative_strength=min(

                10,

                max(

                    0,

                    candidate.relative_strength,

                ),

            ),

            market_score=market["score"],

        )

        return self.recommendation.generate(

            symbol=candidate.symbol,

            technical=intelligence["technical"],

            fundamental=intelligence["fundamental"],

            news=intelligence["news"],

            sector=intelligence["sector"],

            risk=intelligence["risk"],

            confidence=intelligence["confidence"],

            trade_setup=setup,

            trade_type=trade,

        )