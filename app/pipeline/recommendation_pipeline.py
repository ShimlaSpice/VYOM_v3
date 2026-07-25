"""
Recommendation Pipeline for VYOM.

Converts ScanCandidate -> Recommendation
"""

from __future__ import annotations

from app.trade_intelligence import (
    ATREngine,
    TradeClassifier,
    SetupGenerator,
)

from app.intelligence import (
    IntelligenceEngine,
    MarketTrendEngine,
    NewsSentimentEngine,
)

from app.recommendation import RecommendationEngineV2


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

        closes = [c["close"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        volumes = [c["volume"] for c in candles]

        candidate.price = closes[-1]

        candidate.volume = volumes[-1]

        atr = self.atr_engine.summary(

            highs,

            lows,

            closes,

        )

        candidate.atr = atr["atr"]

        market_trend = self.market_trend.evaluate(

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

            atr_percent=atr["atr_percent"],

            trend=market_trend["trend"],

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

                "sma": closes[-1] > candidate.sma20,

                "ema": closes[-1] > candidate.ema20,

                "breakout": closes[-1] >= max(highs[-20:]),

                "volume": candidate.volume > (
                    sum(volumes[-20:]) / min(20, len(volumes))
                ) * 1.5,

            },

            fundamental_input={

                "pe": fundamentals.get("pe"),

                "eps": fundamentals.get("eps"),

                "roe": fundamentals.get("roe"),

                "debt_to_equity": fundamentals.get(
                    "debt_to_equity"
                ),

                "market_cap": fundamentals.get(
                    "market_cap"
                ),

            },

            news_input={

                "sentiment": news_analysis["sentiment"],

                "confidence": news_analysis["confidence"],

                "headlines": news_analysis["headlines"],

            },

            sector_input={

                "sector": sector,

            },

            risk_input={

                "atr_percent": atr["atr_percent"],

                "volatility": atr["volatility"],

                "risk_reward": setup["risk_reward"],

            },

            relative_strength=candidate.relative_strength,

            market_score=market_trend["score"],

        )

        recommendation = self.recommendation.generate(

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

        return recommendation