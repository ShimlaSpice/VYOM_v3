"""
Scanner Engine for VYOM.
"""

from __future__ import annotations

from app.market import MarketDataProvider
from app.scanner.decision_engine import DecisionEngine
from app.scanner.ranking import RankingEngine
from app.ai import AIAnalyst
from app.scanner.models import ScanCandidate, ScanResult
from app.scanner.technical_indicators import TechnicalIndicators


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

            sma20 = TechnicalIndicators.sma(closes, 20)
            ema20 = TechnicalIndicators.ema(closes, 20)

            score = 0

            if closes[-1] > sma20:
                score += 25

            if closes[-1] > ema20:
                score += 25

            candidate = ScanCandidate(
                symbol=symbol,
                score=score,
            )

            candidate = self.decision_engine.evaluate(candidate)
            candidate = self.ai_analyst.analyze(candidate)

            result.candidates.append(candidate)

        result.candidates = self.ranking_engine.rank(
            result.candidates
        )

        return result