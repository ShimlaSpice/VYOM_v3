"""
Scanner Engine for VYOM.
"""

from __future__ import annotations

from datetime import datetime

from app.ai.analyst import AIAnalyst
from app.market import MarketDataProvider
from app.scanner.decision_engine import DecisionEngine
from app.scanner.models import (
    ScanCandidate,
    ScanResult,
)
from app.scanner.ranking import RankingEngine
from app.scanner.relative_strength import RelativeStrength
from app.scanner.scorecard import ScoreCard
from app.scanner.technical_indicators import (
    TechnicalIndicators,
)
from app.universe.universe_engine import (
    UniverseEngine,
)
from concurrent.futures import ThreadPoolExecutor

class ScannerEngine:

    def __init__(

        self,

        provider: MarketDataProvider,

    ):

        self.provider = provider

        self.decision_engine = DecisionEngine()

        self.ranking_engine = RankingEngine()

        self.ai_analyst = AIAnalyst()

        self.universe = UniverseEngine()

    def scan(

        self,

        filters: dict | None = None,

    ) -> ScanResult:

        if filters is None:

            filters = {}

        universe = filters.get(

            "universe",

            "NIFTY50",

        )

        result = ScanResult(

            generated_at=datetime.now().isoformat(),

        )

        symbols = self.universe.get_universe(

            universe,

        )

        if not symbols:

            return result

        self.provider.prefetch(

            symbols,

            period="3mo",

            interval="1d",

        )

        min_price = self._get_min_price(

            filters,

        )

        max_price = self._get_max_price(

            filters,

        )

        with ThreadPoolExecutor(max_workers=12) as executor:
            candidates = executor.map(
                lambda symbol: self._scan_symbol(
                    symbol,
                    min_price,
                    max_price,
                ),
                symbols,

            )
        for candidate in candidates:
            if candidate is not None:
                result.candidates.append(
                    candidate,
                )




        result.candidates = self.ranking_engine.rank(

            result.candidates,

        )

        return result

    def _scan_symbol(

        self,

        symbol: str,

        min_price: float,

        max_price: float,

    ) -> ScanCandidate | None:

        candles = self.provider.get_candles(

            symbol=symbol,

            interval="1d",

            limit=100,

        )

        if len(candles) < 50:

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

        volumes = [

            c["volume"]

            for c in candles

        ]

        latest_price = closes[-1]

        if latest_price < min_price:

            return None

        if max_price > 0 and latest_price > max_price:

            return None

        latest_volume = volumes[-1]

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

        average_volume = TechnicalIndicators.average_volume(

            volumes,

        )

        breakout = TechnicalIndicators.breakout(

            highs,

            latest_price,

        )

        stock_change = TechnicalIndicators.price_change(

            latest_price,

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

                latest_price > sma20,

            "Price above SMA20",

        )

        scorecard.add(

            "sma50",

            latest_price > sma50,

            "Price above SMA50",

        )

        scorecard.add(

            "ema20",

            latest_price > ema20,

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

            f"Positive MACD ({macd:.2f})",

        )

        scorecard.add(

            "volume",

            latest_volume > average_volume * 1.5,

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

            reasons=list(

                scorecard.reasons,

            ),

            price=latest_price,

            volume=latest_volume,

            rsi=rsi,

            macd=macd,

            sma20=sma20,

            sma50=sma50,

            ema20=ema20,

            relative_strength=relative_strength,

        )

        candidate.average_volume = average_volume

        candidate.breakout = breakout

        candidate = self.decision_engine.evaluate(

            candidate,

        )

        candidate = self.ai_analyst.analyze(

            candidate,

        )

        return candidate

    def _get_min_price(

        self,

        filters: dict,

    ) -> float:

        value = filters.get(

            "min_price",

            "",

        )

        if value:

            try:

                return float(value)

            except ValueError:

                pass

        band = filters.get(

            "price_band",

            "All",

        )

        mapping = {

            "Below ₹100": (0, 100),

            "₹100 - ₹500": (100, 500),

            "₹500 - ₹1,000": (500, 1000),

            "₹1,000 - ₹5,000": (1000, 5000),

            "Above ₹5,000": (5000, 0),

        }

        return mapping.get(

            band,

            (0, 0),

        )[0]

    def _get_max_price(

        self,

        filters: dict,

    ) -> float:

        value = filters.get(

            "max_price",

            "",

        )

        if value:

            try:

                return float(value)

            except ValueError:

                pass

        band = filters.get(

            "price_band",

            "All",

        )

        mapping = {

            "Below ₹100": (0, 100),

            "₹100 - ₹500": (100, 500),

            "₹500 - ₹1,000": (500, 1000),

            "₹1,000 - ₹5,000": (1000, 5000),

            "Above ₹5,000": (5000, 0),

        }

        return mapping.get(

            band,

            (0, 0),

        )[1]