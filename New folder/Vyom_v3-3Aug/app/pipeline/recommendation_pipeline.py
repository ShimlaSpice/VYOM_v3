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

        if len(candles) < 20:

            return None

        closes = [

            c["close"]

            for c in candles

        ]

        highs = [

            c["high"]

            for c in candles

        ]

        lows = [

            c["low"]

            for c in candles

        ]

        atr_summary = self.atr_engine.summary(

            highs,

            lows,

            closes,

        )

        market = self.market_trend.evaluate(

            closes,

        )

        headlines = news.get(

            "headlines",

            [],

        )

        news_analysis = self.news_sentiment.evaluate(

            headlines,

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

                "volume": candidate.volume > candidate.average_volume,

            },

            fundamental_input={

                "pe": fundamentals.get("pe"),

                "eps": fundamentals.get("eps"),

                "roe": fundamentals.get("roe"),

                "debt_to_equity": fundamentals.get("debt_to_equity"),

                "market_cap": fundamentals.get("market_cap", 0),

            },

            news_input={
                "sentiment": news_analysis.get(
                    "sentiment",

                    "NEUTRAL",
                ),

                "confidence": news_analysis.get(
                    "confidence",

                    0.50,
                ),

                "headlines": news_analysis.get(
                    "headlines",
                    headlines,
                ),

            },
            sector_input={

                "sector": sector,

            },

            risk_input={

                "atr_percent": atr_summary["atr_percent"],

                "volatility": atr_summary["volatility"],

                "risk_reward": setup["risk_reward"],

            },

            relative_strength=max(

                0,

                min(

                    candidate.relative_strength,

                    10,

                ),

            ),

            market_score=market["score"],

        )

        latest = candles[-1]

        previous = candles[-2]

        close = latest["close"]

        previous_close = previous["close"]

        market_data = {

            "open": latest["open"],

            "high": latest["high"],

            "low": latest["low"],

            "close": close,

            "previous_close": previous_close,

            "change": close - previous_close,

            "change_percent": (

                (close - previous_close)

                / previous_close

                * 100

            ),

            "volume": latest["volume"],

        }

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

            market_data=market_data,

            fundamentals_data=fundamentals,

        )