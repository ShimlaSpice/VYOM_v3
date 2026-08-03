"""
Yahoo Finance Market Data Provider.

The primary, fully-implemented MarketDataProvider. Fetches OHLCV data,
quotes, fundamentals, and market context, backed by a MarketCache
instead of ad hoc instance-level dicts.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd
import yfinance as yf

from app.market.cache import MarketCache
from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader
from core.indicator_pipeline import IndicatorPipeline
from core.market_context import MarketContext

_OHLCV_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


class YahooFinanceProvider(MarketDataProvider):

    def __init__(self, cache: MarketCache | None = None) -> None:
        self.cache = cache or MarketCache()
        self._watchlist_loader = WatchlistLoader()
        self._indicator_pipeline = IndicatorPipeline()

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    # -- internal: single source of truth for a symbol's OHLCV frame --

    def _get_dataframe(

        self,

        symbol: str,

        interval: str = "1d",

        period: str = "1y",

    ) -> pd.DataFrame:

        cache_key = f"{symbol}:{interval}"

        cached = self.cache.get_ohlc(

            cache_key,

        )

        if cached is not None:

            return cached

        df = yf.download(

            tickers=symbol,

            period=period,

            interval=interval,

            progress=False,

            auto_adjust=False,

            threads=True,

            prepost=False,

        )

        if df.empty:

            return df

        if (

            hasattr(df.columns, "nlevels")

            and df.columns.nlevels > 1

        ):

            df.columns = df.columns.get_level_values(0)

        df = df.rename(

            columns={

                "Open": "open",

                "High": "high",

                "Low": "low",

                "Close": "close",

                "Volume": "volume",

            }

        )

        df = df.dropna(

            subset=[

                "open",

                "high",

                "low",

                "close",

                "volume",

            ]

        )

        self.cache.set_ohlc(

            cache_key,

            df,

        )

        return df
    def prefetch(
        self,
        symbols: list[str],
        period: str = "3mo",
        interval: str = "1d",
    ) -> None:
        if not symbols:
            return

        data = yf.download(
            symbols,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False,
            threads=False,
            group_by="ticker",
        )

        if data.empty:
            return

        is_multi = isinstance(data.columns, pd.MultiIndex)

        for symbol in symbols:
            try:
                frame = data[symbol].copy() if is_multi else data.copy()
                if hasattr(frame.columns, "nlevels") and frame.columns.nlevels > 1:
                    frame.columns = frame.columns.get_level_values(0)
                frame = frame.dropna(subset=_OHLCV_COLUMNS)
                if not frame.empty:
                    self.cache.set_ohlc(f"{symbol}:{interval}", frame)
            except Exception:
                continue

    def get_quote(self, symbol: str) -> dict[str, Any]:
        cached = self.cache.get_quote(symbol)
        if cached is not None:
            return cached

        ticker = yf.Ticker(symbol)
        try:
            info = ticker.fast_info
        except Exception:
            info = {}

        quote = {
            "symbol": symbol,
            "last_price": info.get("lastPrice"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "volume": info.get("lastVolume"),
        }
        self.cache.set_quote(symbol, quote)
        return quote

    def get_bulk_quotes(self, symbols: list[str]) -> dict[str, Any]:
        return {symbol: self.get_quote(symbol) for symbol in symbols}

    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        df = self._get_dataframe(symbol, interval=interval)
        if df.empty:
            return []

        candles: list[dict[str, Any]] = []
        for index, row in df.tail(limit).iterrows():
            try:
                open_price = float(row["Open"])
                high_price = float(row["High"])
                low_price = float(row["Low"])
                close_price = float(row["Close"])
                volume = int(row["Volume"])
            except Exception:
                continue

            if any(math.isnan(v) for v in (open_price, high_price, low_price, close_price)):
                continue

            candles.append({
                "timestamp": index,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
            })

        return candles

    def get_market_context(self, symbol: str) -> MarketContext | None:
        """Build the full MarketContext the Scanner and downstream
        engines rely on: OHLCV + indicators + fundamentals + news."""
        df = self._get_dataframe(symbol, interval="1d", period="1y")
        if df.empty or len(df) < 20:
            return None

        cache_key = f"{symbol}:1d"
        indicators = self.cache.get_indicator(cache_key)
        if indicators is None:
            indicators = self._indicator_pipeline.calculate(df)
            self.cache.set_indicator(cache_key, indicators)

        return MarketContext.from_dataframe(
            symbol=symbol,
            dataframe=df,
            indicators=indicators,
            fundamentals=self.get_fundamentals(symbol),
            news=self.get_news(symbol),
        )

    def get_fundamentals(self, symbol: str) -> dict[str, Any]:
        cached = self.cache.get_fundamentals(symbol)
        if cached is not None:
            return cached

        ticker = yf.Ticker(symbol)
        try:
            info = ticker.info
        except Exception:
            return {}

        fundamentals = {
            "symbol": symbol,
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": info.get("marketCap", 0),
            "pe": info.get("trailingPE", 0),
            "forward_pe": info.get("forwardPE", 0),
            "eps": info.get("trailingEps", 0),
            "roe": info.get("returnOnEquity", 0),
            "debt_to_equity": info.get("debtToEquity"),
            "book_value": info.get("bookValue", 0),
            "dividend_yield": info.get("dividendYield", 0),
        }
        self.cache.set_fundamentals(symbol, fundamentals)
        return fundamentals

    def get_news(self, symbol: str) -> dict[str, Any]:
        # Real news integration belongs to the News module (app/news).
        # This stays a stub until that module is rebuilt and wired in.
        return {"headlines": []}

    def get_watchlist(self, universe: str = "nifty50") -> list[str]:
        return self._watchlist_loader.load(f"{universe.lower()}.txt", limit=None)

    def get_market_status(self) -> dict[str, Any]:
        return {"status": "UNKNOWN"}