"""
Yahoo Finance Market Data Provider.
"""

from __future__ import annotations

from typing import Any

import math
import pandas as pd
import yfinance as yf

from app.market.batch_downloader import BatchDownloader
from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader


class YahooFinanceProvider(MarketDataProvider):

    WATCHLIST_LIMIT = 10

    def __init__(self):

        self.batch = BatchDownloader()

        self.cache = None

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def prefetch(

        self,

        symbols: list[str],

        period: str = "3mo",

        interval: str = "1d",

    ) -> None:

        self.cache = self.batch.download(

            symbols,

            period,

            interval,

        )

    def get_quote(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        ticker = yf.Ticker(symbol)

        try:

            info = ticker.fast_info

        except Exception:

            info = {}

        return {

            "symbol": symbol,

            "last_price": info.get("lastPrice"),

            "day_high": info.get("dayHigh"),

            "day_low": info.get("dayLow"),

            "volume": info.get("lastVolume"),

        }

    def _history_from_cache(

        self,

        symbol: str,

    ):

        if self.cache is None:

            return None

        try:

            if isinstance(

                self.cache.columns,

                pd.MultiIndex,

            ):

                if symbol not in self.cache.columns.get_level_values(0):

                    return None

                return self.cache[symbol]

        except Exception:

            pass

        return None

    def get_candles(

        self,

        symbol: str,

        interval: str,

        limit: int = 100,

    ) -> list[dict[str, Any]]:

        history = self._history_from_cache(

            symbol,

        )

        if history is None:

            history = yf.download(

                symbol,

                period="3mo",

                interval=interval,

                progress=False,

                auto_adjust=False,

                threads=False,

            )

        if history.empty:

            return []

        if (

            hasattr(

                history.columns,

                "nlevels",

            )

            and history.columns.nlevels > 1

        ):

            history.columns = history.columns.get_level_values(0)

        history = history.dropna(

            subset=[

                "Open",

                "High",

                "Low",

                "Close",

                "Volume",

            ]

        )

        candles = []

        for index, row in history.tail(limit).iterrows():

            try:

                open_price = float(row["Open"])

                high_price = float(row["High"])

                low_price = float(row["Low"])

                close_price = float(row["Close"])

                volume = int(row["Volume"])

            except Exception:

                continue

            if any(

                math.isnan(value)

                for value in [

                    open_price,

                    high_price,

                    low_price,

                    close_price,

                ]

            ):

                continue

            candles.append(

                {

                    "timestamp": index,

                    "open": open_price,

                    "high": high_price,

                    "low": low_price,

                    "close": close_price,

                    "volume": volume,

                }

            )

        return candles

    def get_fundamentals(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        ticker = yf.Ticker(symbol)

        try:

            info = ticker.info

        except Exception:

            return {}

        return {

            "symbol": symbol,

            "sector": info.get(

                "sector",

                "Unknown",

            ),

            "industry": info.get(

                "industry",

                "Unknown",

            ),

            "market_cap": info.get(

                "marketCap",

                0,

            ),

            "pe": info.get(

                "trailingPE",

                0,

            ),

            "forward_pe": info.get(

                "forwardPE",

                0,

            ),

            "eps": info.get(

                "trailingEps",

                0,

            ),

            "roe": info.get(

                "returnOnEquity",

                0,

            ),

            "debt_to_equity": info.get(

                "debtToEquity",

                None,

            ),

            "book_value": info.get(

                "bookValue",

                0,

            ),

            "dividend_yield": info.get(

                "dividendYield",

                0,

            ),

        }

    def get_watchlist(

        self,

    ) -> list[str]:

        loader = WatchlistLoader()

        return loader.load(

            "nifty50.txt",

            limit=self.WATCHLIST_LIMIT,

        )