"""
NSE Market Data Provider for VYOM.

Version 1
"""

from __future__ import annotations

from typing import Any

import requests

from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader


class NSEProvider(MarketDataProvider):

    BASE_URL = "https://www.nseindia.com"

    API_QUOTE = (
        "https://www.nseindia.com/api/quote-equity"
    )

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(

            {

                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                ),

                "Accept": "application/json",

                "Referer": self.BASE_URL,

            }

        )

    def connect(

        self,

    ) -> None:

        self.session.get(

            self.BASE_URL,

            timeout=10,

        )

    def disconnect(

        self,

    ) -> None:

        self.session.close()

    def prefetch(

        self,

        symbols: list[str],

        period: str = "3mo",

        interval: str = "1d",

    ) -> None:

        pass

    def get_quote(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        symbol = symbol.replace(

            ".NS",

            "",

        )

        try:

            response = self.session.get(

                self.API_QUOTE,

                params={

                    "symbol": symbol,

                },

                timeout=10,

            )

            data = response.json()

        except Exception:

            return {}

        info = data.get(

            "priceInfo",

            {},

        )

        return {

            "symbol": symbol,

            "open": info.get(

                "open",

            ),

            "high": info.get(

                "intraDayHighLow",

                {},

            ).get(

                "max",

            ),

            "low": info.get(

                "intraDayHighLow",

                {},

            ).get(

                "min",

            ),

            "last_price": info.get(

                "lastPrice",

            ),

            "previous_close": info.get(

                "previousClose",

            ),

            "change": info.get(

                "change",

            ),

            "change_percent": info.get(

                "pChange",

            ),

        }

    def get_bulk_quotes(

        self,

        symbols: list[str],

    ) -> dict[str, Any]:

        quotes = {}

        for symbol in symbols:

            quotes[symbol] = self.get_quote(

                symbol,

            )

        return quotes

    def get_candles(

        self,

        symbol: str,

        interval: str,

        limit: int = 100,

    ) -> list[dict[str, Any]]:

        return []

    def get_fundamentals(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        return {}

    def get_news(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        return {

            "headlines": [],

        }

    def get_watchlist(

        self,

        universe: str = "nifty50",

    ) -> list[str]:

        loader = WatchlistLoader()

        return loader.load(

            f"{universe.lower()}.txt",

            limit=None,

        )

    def get_market_status(

        self,

    ) -> dict[str, Any]:

        return {

            "status": "UNKNOWN",

        }

    def get_indices(

        self,

    ) -> dict[str, Any]:

        return {}

    def get_sector_data(

        self,

    ) -> dict[str, Any]:

        return {}

    def get_fii_dii_data(

        self,

    ) -> dict[str, Any]:

        return {}

    def get_corporate_actions(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        return {}

    def get_insider_trades(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        return {}

    def get_market_breadth(

        self,

    ) -> dict[str, Any]:

        return {}