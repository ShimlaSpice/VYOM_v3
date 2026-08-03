"""
Provider Manager for VYOM.

Delegates to an active MarketDataProvider, with a small per-symbol
MarketContext cache so repeated scans in one session don't refetch.
Fixes a previously broken import (app.market.providers.yahoo_provider,
a path that doesn't exist) and drops delegation for the satellite
methods removed from MarketDataProvider — use the dedicated satellite
provider classes directly for those.
"""

from __future__ import annotations

from typing import Any

from app.market.market_data_provider import MarketDataProvider
from app.market.yahoo_provider import YahooFinanceProvider
from core.market_context import MarketContext


class ProviderManager(MarketDataProvider):

    def __init__(self) -> None:
        self.providers: list[MarketDataProvider] = [YahooFinanceProvider()]
        self.active_provider = self.providers[0]
        self._contexts: dict[str, MarketContext] = {}

    def connect(self) -> None:
        try:
            self.active_provider.connect()
        except Exception:
            pass

    def disconnect(self) -> None:
        self.active_provider.disconnect()

    def warmup(

        self,

        symbols: list[str],

        period: str = "6mo",

        interval: str = "1d",

    ) -> None:

        self.prefetch(

            symbols,

            period,

            interval,

        )

        for symbol in symbols:

            try:

                self.get_market_context(

                    symbol,

                )

            except Exception:

                pass


    

    def prefetch(

        self,

        symbols: list[str],

        period: str = "6mo",

        interval: str = "1d",

    ) -> None:

        self.clear_context_cache()

        self.active_provider.prefetch(

            symbols=symbols,

            period=period,

            interval=interval,

        )
    def get_market_context(

        self,

        symbol: str,

    ) -> MarketContext | None:

        context = self._contexts.get(symbol)

        if context is not None:

            return context

        try:
            context = self.active_provider.get_market_context(symbol)
        except Exception:
            return None

        if context is None:
            return None

        self._contexts[symbol] = context
        return context
    def clear_context_cache(self) -> None:
        self._contexts.clear()

    def get_quote(self, symbol: str) -> dict[str, Any]:
        return self.active_provider.get_quote(symbol)

    def get_bulk_quotes(self, symbols: list[str]) -> dict[str, Any]:
        return self.active_provider.get_bulk_quotes(symbols)

    def get_candles(
        self, symbol: str, interval: str, limit: int = 100,
    ) -> list[dict[str, Any]]:
        return self.active_provider.get_candles(symbol, interval, limit)

    def get_fundamentals(self, symbol: str) -> dict[str, Any]:
        return self.active_provider.get_fundamentals(symbol)

    def get_news(self, symbol: str) -> dict[str, Any]:
        return self.active_provider.get_news(symbol)

    def get_watchlist(self, universe: str = "nifty50") -> list[str]:
        return self.active_provider.get_watchlist(universe)

    def get_market_status(self) -> dict[str, Any]:
        return self.active_provider.get_market_status()