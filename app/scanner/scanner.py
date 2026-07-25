"""
Scanner Engine for VYOM.
"""

from __future__ import annotations

from app.market import MarketDataProvider
from app.scanner.decision_engine import DecisionEngine
from app.scanner.ranking import RankingEngine
from app.ai.analyst import AIAnalyst
from app.scanner.models import ScanCandidate, ScanResult
from app.scanner.technical_indicators import TechnicalIndicators
from app.scanner.scorecard import ScoreCard
from app.scanner.relative_strength import RelativeStrength
from app.universe.universe_engine import UniverseEngine


class ScannerEngine:

    def __init__(

        self,

        provider: MarketDataProvider,

    ):

        self.provider = provider

        self.decision_engine = DecisionEngine()

        self.ranking_engine = RankingEngine()

        self.ai_analyst = AIAnalyst()

    def scan(

        self,

    ) -> ScanResult:

        result = ScanResult(

            generated_at="",

        )
        universe = UniverseEngine()

        symbols = universe.get_universe(
            "Nifty50",
        )

        self.provider.prefetch(
            symbols,

            period="3mo",

            interval="1d",
            
        )

        for symbol in symbols:

            candles = self.provider.get_candles(

                symbol=symbol,

                interval="1d",

                limit=100,

            )

            if len(candles) < 50:

                continue

            closes = [c["close"] for c in candles]
            highs = [c["high"] for c in candles]
            lows = [c["low"] for c in candles]
            volumes = [c["volume"] for c in candles]

            sma20 = TechnicalIndicators.sma(
                closes,
                20,
            )

            sma50 = TechnicalIndicators.sma(
                closes,
                50,
            )

            ema20 = TechnicalIndicators.ema(
                closes,
                20,
            )

            rsi = TechnicalIndicators.rsi(
                closes,
            )

            macd, signal = TechnicalIndicators.macd(
                closes,
            )

            avg_volume = TechnicalIndicators.average_volume(
                volumes,
            )

            breakout = TechnicalIndicators.breakout(
                highs,
                closes[-1],
            )

            stock_change = TechnicalIndicators.price_change(

                closes[-1],

                closes[-2],

            )

            market_change = 0.0

            relative_strength = RelativeStrength.calculate(

                stock_change,

                market_change,

            )

            scorecard = ScoreCard()

            scorecard.add(

                "sma20",

                closes[-1] > sma20,

                "Price above SMA20",

            )

            scorecard.add(

                "sma50",

                closes[-1] > sma50,

                "Price above SMA50",

            )

            scorecard.add(

                "ema20",

                closes[-1] > ema20,

                "Price above EMA20",

            )

            scorecard.add(

                "rsi",

                45 <= rsi <= 65,

                f"Healthy RSI ({rsi:.2f})",

            )

            scorecard.add(

                "macd",

                macd > signal,

                f"Bullish MACD ({macd:.2f})",

            )

            scorecard.add(

                "volume",

                volumes[-1] > avg_volume * 1.5,

                "Volume Spike",

            )

            scorecard.add(

                "breakout",

                breakout,

                "20-Day Breakout",

            )

            scorecard.add(

                "relative_strength",

                relative_strength > 1,

                f"Relative Strength ({relative_strength:.2f})",

            )

            candidate = ScanCandidate(

                symbol=symbol,

                score=scorecard.total,

                reasons=list(scorecard.reasons),

                price=closes[-1],

                volume=volumes[-1],

                rsi=rsi,

                macd=macd,

                sma20=sma20,

                sma50=sma50,

                ema20=ema20,

                relative_strength=relative_strength,
                

            )

            candidate = self.decision_engine.evaluate(

                candidate,

            )

            candidate = self.ai_analyst.analyze(

                candidate,

            )

            result.candidates.append(

                candidate,

            )

        result.candidates = self.ranking_engine.rank(

            result.candidates,

        )

        return result