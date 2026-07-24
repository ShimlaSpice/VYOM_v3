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

        # -----------------------------------------------------
        # ATR
        # -----------------------------------------------------

        atr = self.atr_engine.summary(

            highs,

            lows,

            closes,

        )

        # -----------------------------------------------------
        # Trade Classification
        # -----------------------------------------------------

        market_trend = MarketTrendEngine().evaluate(
            closes
        )

        news_analysis = NewsSentimentEngine().evaluate(
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

        # -----------------------------------------------------
        # Trade Setup
        # -----------------------------------------------------

        setup = SetupGenerator().generate(

            highs,

            lows,

            closes,

            trade["category"],

        )

        # -----------------------------------------------------
        # Intelligence
        # -----------------------------------------------------

        intelligence = self.intelligence.analyze(

            technical_input={

                "score": candidate.score,

                "rsi": fundamentals.get("rsi", 50),

                "macd": fundamentals.get("macd", 0),

                "sma": True,

                "ema": True,

                "breakout": False,

                "volume": False,

            },

            fundamental_input={

                "pe": fundamentals.get("pe", 25),

                "eps": fundamentals.get("eps", 10),

                "roe": fundamentals.get("roe", 15),

                "debt_to_equity":
                    fundamentals.get(
                        "debt_to_equity",
                        50,
                    ),

                "market_cap":
                    fundamentals.get(
                        "market_cap",
                        0,
                    ),

            },

            news_input = {

                "sentiment": news_analysis["sentiment"],

                "confidence": news_analysis["confidence"],

                "headlines": news_analysis["headlines"],

            },

            risk_input={

                "atr_percent":
                    atr["atr_percent"],

                "volatility":
                    atr["volatility"],

                "risk_reward":
                    setup["risk_reward"],

            },

            relative_strength=8,

            market_score=8,

        )

        # -----------------------------------------------------
        # Recommendation
        # -----------------------------------------------------

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