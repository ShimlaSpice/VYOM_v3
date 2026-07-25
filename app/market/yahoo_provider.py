"""
Yahoo Finance Market Data Provider.
"""

from __future__ import annotations

from typing import Any

import yfinance as yf

from app.market.batch_downloader import BatchDownloader
from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader


class YahooFinanceProvider(MarketDataProvider):

    WATCHLIST_LIMIT = 10

    def __init__(self):

        self.batch = BatchDownloader()

        self.cache = {}

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def prefetch(

        self,

        symbols: list[str],

        period: str = "3mo",

        interval: str = "1d",

    ):

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

    def get_candles(

        self,

        symbol: str,

        interval: str,

        limit: int = 100,

    ) -> list[dict[str, Any]]:

        if self.cache is not None and symbol in self.cache.columns.get_level_values(0):

            history = self.cache[symbol]

        else:

            history = yf.download(

                symbol,

                period="3mo",

                interval=interval,

                progress=False,

                auto_adjust=False,

            )

        if history.empty:

            return []

        if hasattr(history.columns, "nlevels") and history.columns.nlevels > 1:

            history.columns = history.columns.get_level_values(0)

        candles = []

        for index, row in history.tail(limit).iterrows():

            candles.append(

                {

                    "timestamp": index,

                    "open": float(row["Open"]),

                    "high": float(row["High"]),

                    "low": float(row["Low"]),

                    "close": float(row["Close"]),

                    "volume": int(row["Volume"]),

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

            "sector": info.get("sector", "Unknown"),

            "industry": info.get("industry", "Unknown"),

            "market_cap": info.get("marketCap", 0),

            "pe": info.get("trailingPE", 0),

            "forward_pe": info.get("forwardPE", 0),

            "eps": info.get("trailingEps", 0),

            "roe": info.get("returnOnEquity", 0),

            "debt_to_equity": info.get("debtToEquity", 0),

            "book_value": info.get("bookValue", 0),

            "dividend_yield": info.get("dividendYield", 0),

        }

    def get_watchlist(

        self,

    ) -> list[str]:

        loader = WatchlistLoader()

        return loader.load(

            "nifty50.txt",

            limit=self.WATCHLIST_LIMIT,

        )