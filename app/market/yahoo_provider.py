"""
Yahoo Finance Market Data Provider.
"""

from __future__ import annotations

from typing import Any

import yfinance as yf

from app.market.market_data_provider import MarketDataProvider
from app.market.watchlist_loader import WatchlistLoader


class YahooFinanceProvider(MarketDataProvider):

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def get_quote(self, symbol: str) -> dict[str, Any]:

        ticker = yf.Ticker(symbol)

        info = ticker.fast_info

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

        history = yf.download(
            symbol,
            period="3mo",
            interval=interval,
            progress=False,
            auto_adjust=False,
        )

        if history.empty:
            return []
        
        # Handle MultiIndex returned by newer yfinance versions
        if hasattr(history.columns, "nlevels") and history.columns.nlevels > 1:
            history.columns = history.columns.get_level_values(0)

        candles = []

        for index, row in history.tail(limit).iterrows():
            candle = {
                "timestamp": index,
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
            
            candles.append(candle)

        return candles

    def get_watchlist(self) -> list[str]:
        loader = WatchlistLoader()
        return loader.load("nifty50.txt")