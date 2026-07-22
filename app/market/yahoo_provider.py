"""
Yahoo Finance implementation.
"""

from __future__ import annotations

from app.market.market_data_provider import MarketDataProvider


class YahooFinanceProvider(MarketDataProvider):

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def get_quote(self, symbol: str):
        return {}

    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ):
        return []

    def get_watchlist(self):
        return []