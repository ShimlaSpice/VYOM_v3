"""
VYOM Intelligence Engine.

Central orchestrator for all intelligence modules.
"""

from __future__ import annotations

from core.market_context import MarketContext

from app.ai.jarvis_engine import JarvisEngine
from app.intelligence.confidence_engine import ConfidenceEngine
from app.intelligence.fundamental_engine import FundamentalEngine
from app.intelligence.news_engine import NewsEngine
from app.intelligence.risk_engine import RiskEngine
from app.intelligence.sector_engine import SectorEngine
from app.intelligence.technical_engine import TechnicalEngine


class IntelligenceEngine:

    def __init__(self):

        self.technical = TechnicalEngine()

        self.fundamental = FundamentalEngine()

        self.news = NewsEngine()

        self.sector = SectorEngine()

        self.risk = RiskEngine()

        self.confidence = ConfidenceEngine()

        self.jarvis = JarvisEngine()

    def analyze(

        self,

        context: MarketContext | None = None,

        technical_input: dict | None = None,

        fundamental_input: dict | None = None,

        news_input: dict | None = None,

        sector_input: dict | None = None,

        risk_input: dict | None = None,

        relative_strength: float = 0,

        market_score: float = 0,

    ) -> dict:

        technical_input = technical_input or {}

        fundamental_input = fundamental_input or {}

        news_input = news_input or {}

        sector_input = sector_input or {}

        risk_input = risk_input or {}

        if context is not None:

            indicators = context.indicators

            technical_input = {

                "score": 0,

                "rsi": indicators["rsi"],

                "macd": indicators["macd"],

                "sma": context.close > indicators["sma20"],

                "ema": context.close > indicators["ema20"],

                "breakout": indicators["breakout"],

                "volume": indicators["volume_ratio"] >= 1.20,

            }

            risk_input = {

                "atr_percent": indicators["atr_percent"],

                "volatility": indicators["volatility"],

                "risk_reward": fundamental_input.get(

                    "risk_reward",

                    2.0,

                ),

            }

        technical = self.technical.evaluate(

            **technical_input,

        )

        fundamental = self.fundamental.evaluate(

            **fundamental_input,

        )

        news = self.news.evaluate(

            **news_input,

        )

        sector = self.sector.evaluate(

            **sector_input,

        )

        risk = self.risk.evaluate(

            **risk_input,

        )

        confidence = self.confidence.calculate(

            technical=technical["score"],

            fundamental=fundamental["score"],

            news=news["score"],

            sector=sector["score"],

            relative_strength=relative_strength,

            market=market_score,

            risk=risk["score"],

        )

        jarvis = self.jarvis.analyze(

            technical=technical,

            fundamental=fundamental,

            news=news,

            sector=sector,

            risk=risk,

            confidence=confidence,

        )

        return {

            "context": context,

            "technical": technical,

            "fundamental": fundamental,

            "news": news,

            "sector": sector,

            "risk": risk,

            "confidence": confidence,

            "jarvis": jarvis,

        }