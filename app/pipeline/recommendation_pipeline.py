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
            float(c.get("close", 0.0))
            for c in candles
            if isinstance(c, dict)
        ]

        highs = [
            float(c.get("high", 0.0))
            for c in candles
            if isinstance(c, dict)
        ]

        lows = [
            float(c.get("low", 0.0))
            for c in candles
            if isinstance(c, dict)
        ]

        if not closes or not highs or not lows:
            return None

        atr_summary = self.atr_engine.summary(
            highs,
            lows,
            closes,
        )

        market = self.market_trend.evaluate(closes)

        headlines = list(news.get("headlines", []))
        news_analysis = self.news_sentiment.evaluate(headlines)

        trade = self.trade_classifier.classify(
            score=getattr(candidate, "score", 0),
            atr_percent=atr_summary.get("atr_percent", 0.0),
            trend=market.get("trend", "NEUTRAL"),
            sentiment=news_analysis.get("sentiment", "NEUTRAL"),
        )

        setup = self.setup_generator.generate(
            highs,
            lows,
            closes,
            trade.get("category", "WATCH"),
        )

        intelligence = self.intelligence.analyze(
            technical_input={
                "score": getattr(candidate, "score", 0),
                "rsi": getattr(candidate, "rsi", 0),
                "macd": getattr(candidate, "macd", 0),
                "sma": getattr(candidate, "price", 0) > getattr(candidate, "sma20", 0),
                "ema": getattr(candidate, "price", 0) > getattr(candidate, "ema20", 0),
                "breakout": getattr(candidate, "breakout", False),
                "volume": getattr(candidate, "volume", 0) > getattr(candidate, "average_volume", 0),
            },
            fundamental_input={
                "pe": fundamentals.get("pe"),
                "eps": fundamentals.get("eps"),
                "roe": fundamentals.get("roe"),
                "debt_to_equity": fundamentals.get("debt_to_equity"),
                "market_cap": fundamentals.get("market_cap", 0),
            },
            news_input={
                "sentiment": news_analysis.get("sentiment", "NEUTRAL"),
                "confidence": news_analysis.get("confidence", 0.50),
                "headlines": news_analysis.get("headlines", headlines),
            },
            sector_input={
                "sector": sector,
            },
            risk_input={
                "atr_percent": atr_summary.get("atr_percent", 0.0),
                "volatility": atr_summary.get("volatility", 0.0),
                "risk_reward": setup.get("risk_reward", 0.0),
            },
            relative_strength=max(0, min(getattr(candidate, "relative_strength", 0), 10)),
            market_score=market.get("score", 0),
        )

        latest = candles[-1]
        previous = candles[-2]

        close = float(latest.get("close", 0.0))
        previous_close = float(previous.get("close", 0.0))

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