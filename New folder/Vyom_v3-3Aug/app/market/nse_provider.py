"""
NSE Market Data Provider for VYOM.

Quote-only provider using NSE's public quote API. Deliberately partial:
candle history and market-context building aren't available from this
endpoint, so those methods report that honestly (empty / None) rather
than pretending to work. Not currently the active provider — see
ProviderManager — but kept ready for when NSE integration is extended.
"""

from __future__ import annotations

from typing import Any

import requests

from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader
from core.market_context import MarketContext

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/138.0 Safari/537.36"
)


class NSEProvider(MarketDataProvider):

    BASE_URL = "https://www.nseindia.com"
    API_QUOTE = "https://www.nseindia.com/api/quote-equity"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
            "Referer": self.BASE_URL,
        })
        self._watchlist_loader = WatchlistLoader()

    def connect(self) -> None:
        self.session.get(self.BASE_URL, timeout=10)

    def disconnect(self) -> None:
        self.session.close()

    def prefetch(
        self,
        symbols: list[str],
        period: str = "3mo",
        interval: str = "1d",
    ) -> None:
        pass

    def get_quote(self, symbol: str) -> dict[str, Any]:
        symbol = symbol.replace(".NS", "")
        try:
            response = self.session.get(
                self.API_QUOTE, params={"symbol": symbol}, timeout=10,
            )
            data = response.json()
        except Exception:
            return {}

        info = data.get("priceInfo", {})
        return {
            "symbol": symbol,
            "open": info.get("open"),
            "high": info.get("intraDayHighLow", {}).get("max"),
            "low": info.get("intraDayHighLow", {}).get("min"),
            "last_price": info.get("lastPrice"),
            "previous_close": info.get("previousClose"),
            "change": info.get("change"),
            "change_percent": info.get("pChange"),
        }

    def get_bulk_quotes(self, symbols: list[str]) -> dict[str, Any]:
        return {symbol: self.get_quote(symbol) for symbol in symbols}

    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        # Not available from the NSE quote endpoint.
        return []

    def get_market_context(self, symbol: str) -> MarketContext | None:
        # Requires candle history, which this provider doesn't have.
        return None

    def get_fundamentals(self, symbol: str) -> dict[str, Any]:
        return {}

    def get_news(self, symbol: str) -> dict[str, Any]:
        return {"headlines": []}

    def get_watchlist(self, universe: str = "nifty50") -> list[str]:
        return self._watchlist_loader.load(f"{universe.lower()}.txt", limit=None)

    def get_market_status(self) -> dict[str, Any]:
        return {"status": "UNKNOWN"}