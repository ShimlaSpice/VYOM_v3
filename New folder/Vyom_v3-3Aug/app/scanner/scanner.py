"""
Scanner Engine for VYOM.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from app.ai.analyst import AIAnalyst
from app.market import MarketDataProvider
from app.scanner.decision_engine import DecisionEngine
from app.scanner.models import ScanCandidate, ScanResult
from app.scanner.ranking import RankingEngine
from app.scanner.relative_strength import RelativeStrength
from app.scanner.scorecard import ScoreCard
from app.universe.universe_engine import UniverseEngine

_PRICE_BANDS: dict[str, tuple[float, float]] = {
    "Below \u20b9100": (0, 100),
    "\u20b9100 - \u20b9500": (100, 500),
    "\u20b9500 - \u20b91,000": (500, 1000),
    "\u20b91,000 - \u20b95,000": (1000, 5000),
    "Above \u20b95,000": (5000, 0),
}

_BENCHMARK_SYMBOL = "^NSEI"
_MAX_SCAN_WORKERS = 12


class ScannerEngine:

    def __init__(self, provider: MarketDataProvider):
        self.provider = provider
        self.decision_engine = DecisionEngine()
        self.ranking_engine = RankingEngine()
        self.ai_analyst = AIAnalyst()
        self.universe = UniverseEngine()

    def scan(self, filters: dict | None = None) -> ScanResult:
        if filters is None:
            filters = {}

        universe = filters.get(
            "universe",
            "NIFTY50"
        )

        result = ScanResult(
            generated_at=datetime.now().isoformat(),
        )

        symbols = self.universe.get_universe(
            universe,
        )

        symbols = list(
            dict.fromkeys(
                symbols,
            )
        )
        
        if not symbols:
            return result

        if universe.upper() == "ALL":

            symbols = symbols[:1500]

        elif universe.upper() == "NIFTY500":

            symbols = symbols[:500]

        elif universe.upper() == "NIFTY200":

            symbols = symbols[:200]

        elif universe.upper() == "NIFTY100":

            symbols = symbols[:100]

        elif universe.upper() == "NIFTY50":

            symbols = symbols[:50]

        self.provider.prefetch(symbols, period="3mo", interval="1d")

        min_price, max_price = self._price_range(filters)
        market_change = self._benchmark_change()

        workers = min(
            max(
                4,
                len(symbols) // 20,
            ),
            24,
        )
        with ThreadPoolExecutor(max_workers=workers) as executor:
            candidates = executor.map(
                lambda symbol: self._scan_symbol(
                    symbol, min_price, max_price, market_change,
                ),
                symbols,
            )

        for candidate in candidates:
            if candidate is not None:
                result.candidates.append(candidate)

        result.candidates = self.ranking_engine.rank(
            result.candidates,
        )

        if filters.get(
            "top",
        ):
            result.candidates = result.candidates[
                : max(
                    filters["top"] * 5,
                    50,
                )
            ]
        return result

    def _benchmark_change(self) -> float:
        """Today's % change for the NIFTY benchmark, fetched once per
        scan so every symbol's Relative Strength is measured against
        the same reference point rather than 0.0 (the previous bug)."""
        context = self.provider.get_market_context(_BENCHMARK_SYMBOL)
        return context.change_percent if context is not None else 0.0

    def _scan_symbol(

        self,

        symbol: str,

        min_price: float,

        max_price: float,

        market_change: float,

    ) -> ScanCandidate | None:

        context = self.provider.get_market_context(symbol)

        if context is None:

            return None

        latest_price = context.close

        if latest_price < min_price:

            return None

        if max_price > 0 and latest_price > max_price:

            return None

        indicators = context.indicators

    # -------------------------------------------------
    # FAST PRE FILTER
    # Reject weak stocks before AI
    # -------------------------------------------------

        if context.volume < 100000:

            return None

        if indicators["volume_ratio"] < 1.10:

            return None

        if latest_price < indicators["sma20"]:

            return None

        if latest_price < indicators["ema20"]:

            return None

        relative_strength = RelativeStrength.calculate(

            context.change_percent,

            market_change,

        )

        if relative_strength < 0.50:

            return None

        scorecard = ScoreCard()

        scorecard.add(

            "sma20",

            latest_price > indicators["sma20"],

            "Price above SMA20",

        )

        scorecard.add(

            "sma50",

            latest_price > indicators["sma50"],

            "Price above SMA50",

        )

        scorecard.add(

            "ema20",

            latest_price > indicators["ema20"],

            "Price above EMA20",

        )

        scorecard.add(

            "rsi",

            45 <= indicators["rsi"] <= 65,

            f"Healthy RSI ({indicators['rsi']:.2f})",

        )

        scorecard.add(

            "macd",

            indicators["macd"]

            >

            indicators["macd_signal"],

            "Bullish MACD",

        )

        scorecard.add(

            "volume",

            indicators["volume_ratio"] >= 1.50,

            "Volume Spike",

        )

        scorecard.add(

            "breakout",

            indicators["breakout"],

            "Breakout",

        )

        scorecard.add(

            "relative_strength",

            relative_strength > 1,

            "Relative Strength",

        )

        candidate = ScanCandidate(

            symbol=symbol,

            score=scorecard.total,

            reasons=list(scorecard.reasons),

            price=latest_price,

            volume=context.volume,

            rsi=indicators["rsi"],

            macd=indicators["macd"],

            sma20=indicators["sma20"],

            sma50=indicators["sma50"],

            ema20=indicators["ema20"],

            relative_strength=relative_strength,

        )

        candidate.average_volume = (

            context.volume

            /

            max(

                indicators["volume_ratio"],

                1,

            )

        )

        candidate.breakout = indicators["breakout"]

        candidate = self.decision_engine.evaluate(

            candidate,

        )

    # -----------------------------------------
    # AI ONLY FOR GOOD STOCKS
    # -----------------------------------------

        if candidate.score >= 5:

            candidate = self.ai_analyst.analyze(

                candidate,

            )

        return candidate



    def _price_range(self, filters: dict) -> tuple[float, float]:
        """Resolve (min_price, max_price) from explicit overrides or a
        named price band. Replaces the previous _get_min_price /
        _get_max_price pair, which hardcoded the same band table twice."""
        band = filters.get("price_band", "All")
        band_min, band_max = _PRICE_BANDS.get(band, (0, 0))

        min_price = self._parse_price(filters.get("min_price", ""), band_min)
        max_price = self._parse_price(filters.get("max_price", ""), band_max)
        return min_price, max_price

    @staticmethod
    def _parse_price(value: str, fallback: float) -> float:
        if value:
            try:
                return float(value)
            except ValueError:
                pass
        return fallback