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


class ScannerEngine:
    """
    Scans all available symbols and ranks opportunities.
    """

    def __init__(self, provider: MarketDataProvider):
        self.provider = provider
        self.decision_engine = DecisionEngine()
        self.ranking_engine = RankingEngine()
        self.ai_analyst = AIAnalyst()

    def scan(self) -> ScanResult:

        result = ScanResult(generated_at="")

        symbols = self.provider.get_watchlist()

        for symbol in symbols:

            candles = self.provider.get_candles(
                symbol=symbol,
                interval="1d",
                limit=50,
            )

            if not candles:
                continue

            closes = [c["close"] for c in candles]
            highs = [c["high"] for c in candles]
            volumes = [c["volume"] for c in candles]

            # -----------------------------
            # Technical Indicators
            # -----------------------------
            sma20 = TechnicalIndicators.sma(closes, 20)
            ema20 = TechnicalIndicators.ema(closes, 20)
            rsi = TechnicalIndicators.rsi(closes)
            macd, signal = TechnicalIndicators.macd(closes)

            avg_volume = TechnicalIndicators.average_volume(volumes)

            is_breakout = TechnicalIndicators.breakout(
                highs,
                closes[-1],
            )

            # -----------------------------
            # Relative Strength
            # -----------------------------
            stock_change = TechnicalIndicators.price_change(
                closes[-1],
                closes[-2],
            )

            # Temporary
            market_change = 0.0

            relative_strength = RelativeStrength.calculate(
                stock_change,
                market_change,
            )

            # -----------------------------
            # Score Card
            # -----------------------------
            scorecard = ScoreCard()

            scorecard.add(
                "sma",
                closes[-1] > sma20,
                "Price above SMA20",
            )

            scorecard.add(
                "ema",
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
                macd > 0,
                f"MACD Positive ({macd:.2f})",
            )

            scorecard.add(
                "volume",
                volumes[-1] > avg_volume * 1.5,
                f"Volume Spike ({volumes[-1]:,})",
            )

            scorecard.add(
                "breakout",
                is_breakout,
                "20-Day Breakout",
            )

            scorecard.add(
                "momentum",
                relative_strength > 1.0,
                f"Relative Strength ({relative_strength:.2f}%)",
            )

            # -----------------------------
            # Candidate
            # -----------------------------
            candidate = ScanCandidate(
                symbol=symbol,
                score=scorecard.total,
                reasons=list(scorecard.reasons),
            )

            candidate = self.decision_engine.evaluate(candidate)
            candidate = self.ai_analyst.analyze(candidate)

            result.candidates.append(candidate)

        result.candidates = self.ranking_engine.rank(
            result.candidates
        )

        return result