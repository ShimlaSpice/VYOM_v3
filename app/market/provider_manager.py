"""
Provider Manager for VYOM.

Handles multiple market data providers.
"""

from __future__ import annotations

from core.market_context import MarketContext

from app.market.market_data_provider import MarketDataProvider
from app.market.providers.yahoo_provider import YahooFinanceProvider


class ProviderManager(MarketDataProvider):

    def __init__(self) -> None:

        self.providers = [
            YahooFinanceProvider(),
        ]

        self.active_provider = self.providers[0]

        self._contexts: dict[str, MarketContext] = {}

    def connect(self) -> None:

        self.active_provider.connect()

    def disconnect(self) -> None:

        self.active_provider.disconnect()

    def prefetch(
        self,
        symbols: list[str],
        period: str = "3mo",
        interval: str = "1d",
    ) -> None:

        self.active_provider.prefetch(
            symbols,
            period,
            interval,
        )

    def get_market_context(
        self,
        symbol: str,
    ) -> MarketContext:

        if symbol not in self._contexts:

            self._contexts[symbol] = (
                self.active_provider.get_market_context(
                    symbol,
                )
            )

        return self._contexts[symbol]

    def clear_context_cache(self) -> None:

        self._contexts.clear()

    def get_quote(
        self,
        symbol: str,
    ):

        return self.active_provider.get_quote(
            symbol,
        )

    def get_bulk_quotes(
        self,
        symbols: list[str],
    ):

        return self.active_provider.get_bulk_quotes(
            symbols,
        )

    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ):

        return self.active_provider.get_candles(
            symbol,
            interval,
            limit,
        )

    def get_fundamentals(
        self,
        symbol: str,
    ):

        return self.active_provider.get_fundamentals(
            symbol,
        )

    def get_news(
        self,
        symbol: str,
    ):

        return self.active_provider.get_news(
            symbol,
        )

    def get_watchlist(
        self,
        universe: str = "nifty50",
    ):

        return self.active_provider.get_watchlist(
            universe,
        )

    def get_market_status(self):

        return self.active_provider.get_market_status()

    def get_indices(self):

        return self.active_provider.get_indices()

    def get_sector_data(self):

        return self.active_provider.get_sector_data()

    def get_fii_dii_data(self):

        return self.active_provider.get_fii_dii_data()

    def get_corporate_actions(
        self,
        symbol: str,
    ):

        return self.active_provider.get_corporate_actions(
            symbol,
        )

    def get_insider_trades(
        self,
        symbol: str,
    ):

        return self.active_provider.get_insider_trades(
            symbol,
        )

    def get_market_breadth(self):

        return self.active_provider.get_market_breadth()