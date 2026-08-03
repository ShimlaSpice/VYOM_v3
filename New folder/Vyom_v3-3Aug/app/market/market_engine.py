"""
Market Engine for VYOM.
"""

from __future__ import annotations

import time

from app.market import MarketDataProvider
from app.market.validator import MarketDataValidator


class MarketEngine:
    """
    Coordinates market data operations.
    """

    def __init__(self, provider: MarketDataProvider):

        self.provider = provider

        self._cache: dict = {}

    def load_history(

        self,

        symbol: str,

        interval: str = "1d",

        limit: int = 100,

        retries: int = 3,

        delay: int = 2,

    ):

        cache_key = f"{symbol}_{interval}_{limit}"

        if cache_key in self._cache:

            return self._cache[cache_key]

        last_exception = None

        for attempt in range(retries):

            try:

                candles = self.provider.get_candles(

                    symbol=symbol,

                    interval=interval,

                    limit=limit,

                )

                candles = MarketDataValidator.validate_candles(
                    candles
                )

                if candles:

                    self._cache[cache_key] = candles

                    return candles

            except Exception as exc:

                last_exception = exc

                print(
                    f"[MarketEngine] Retry {attempt + 1}/{retries} : {exc}"
                )

                time.sleep(delay)

        if cache_key in self._cache:

            print(
                "[MarketEngine] Using cached data."
            )

            return self._cache[cache_key]

        if last_exception:

            raise last_exception

        return []

    def load_quote(

        self,

        symbol: str,

    ):

        return self.provider.get_quote(symbol)

    def clear_cache(self):

        self._cache.clear()

    def cache_size(self):

        return len(self._cache)