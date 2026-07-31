"""
===========================================================
VYOM AI - Market Data Hub
Sprint 53 - Phase 1

Single source of truth for all market data.

Responsibilities
----------------
✓ Download OHLC only once
✓ Cache DataFrames
✓ Share DataFrame across engines
✓ Multi-timeframe support
✓ Thread-safe
✓ Auto cache expiry
✓ Foundation for Indicator Pipeline
===========================================================
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional

import pandas as pd

try:
    import yfinance as yf
except Exception:
    yf = None


# ==========================================================
# Cache Entry
# ==========================================================

@dataclass
class CacheEntry:

    dataframe: pd.DataFrame

    timestamp: float

    interval: str

    symbol: str


# ==========================================================
# Market Data Hub
# ==========================================================

class MarketDataHub:

    """
    Central Market Data Provider.

    Every module in VYOM should use ONLY this class
    to obtain OHLC data.

    Scanner

        ↓

    Recommendation Engine

        ↓

    AI Engines

        ↓

    Jarvis

        ↓

    Universal Search

        ↓

    UI

    Nobody should call Yahoo directly.
    """

    DEFAULT_PERIOD = "6mo"

    CACHE_SECONDS = {

        "1m": 20,

        "2m": 25,

        "5m": 30,

        "15m": 60,

        "30m": 120,

        "60m": 180,

        "90m": 180,

        "1h": 180,

        "1d": 600,

        "5d": 900,

        "1wk": 1800,

    }

    def __init__(self):

        self._cache: Dict[str, CacheEntry] = {}

        self._lock = threading.RLock()

    # ======================================================
    # Cache Key
    # ======================================================

    @staticmethod
    def _cache_key(symbol: str, interval: str) -> str:

        return f"{symbol.upper()}::{interval}"

    # ======================================================
    # Cache Validation
    # ======================================================

    def _is_valid(self, key: str) -> bool:

        if key not in self._cache:

            return False

        entry = self._cache[key]

        ttl = self.CACHE_SECONDS.get(entry.interval, 300)

        age = time.time() - entry.timestamp

        return age < ttl

    # ======================================================
    # Download
    # ======================================================

    def _download(

        self,

        symbol: str,

        interval: str,

        period: str,

    ) -> pd.DataFrame:

        if yf is None:

            raise RuntimeError(

                "yfinance package not installed."

            )

        ticker = yf.Ticker(symbol)

        df = ticker.history(

            period=period,

            interval=interval,

            auto_adjust=False,

            actions=False,

        )

        if df.empty:

            return pd.DataFrame()

        df = df.rename(

            columns={

                "Open": "open",

                "High": "high",

                "Low": "low",

                "Close": "close",

                "Volume": "volume",

            }

        )

        df.index.name = "datetime"

        return df

    # ======================================================
    # Public Fetch
    # ======================================================

    def get_ohlc(

        self,

        symbol: str,

        interval: str = "1d",

        period: str = DEFAULT_PERIOD,

        force_refresh: bool = False,

    ) -> pd.DataFrame:

        key = self._cache_key(symbol, interval)

        with self._lock:

            if (

                not force_refresh

                and self._is_valid(key)

            ):

                return self._cache[key].dataframe

            df = self._download(

                symbol=symbol,

                interval=interval,

                period=period,

            )

            self._cache[key] = CacheEntry(

                dataframe=df,

                timestamp=time.time(),

                interval=interval,

                symbol=symbol,

            )

            return df

    # ======================================================
    # Bulk Fetch
    # ======================================================

    def get_bulk_ohlc(

        self,

        symbols: list[str],

        interval: str = "1d",

        period: str = DEFAULT_PERIOD,

        force_refresh: bool = False,

    ) -> Dict[str, pd.DataFrame]:

        result: Dict[str, pd.DataFrame] = {}

        for symbol in symbols:

            try:

                result[symbol] = self.get_ohlc(

                    symbol=symbol,

                    interval=interval,

                    period=period,

                    force_refresh=force_refresh,

                )

            except Exception:

                result[symbol] = pd.DataFrame()

        return result
    # ======================================================
    # Refresh
    # ======================================================

    def refresh_symbol(

        self,

        symbol: str,

        interval: str = "1d",

        period: str = DEFAULT_PERIOD,

    ) -> pd.DataFrame:

        return self.get_ohlc(

            symbol=symbol,

            interval=interval,

            period=period,

            force_refresh=True,

        )

    # ======================================================
    # Remove One Cache
    # ======================================================

    def clear_symbol(

        self,

        symbol: str,

        interval: str | None = None,

    ) -> None:

        with self._lock:

            if interval:

                key = self._cache_key(symbol, interval)

                self._cache.pop(key, None)

                return

            symbol = symbol.upper()

            remove_keys = [

                key

                for key in self._cache

                if key.startswith(symbol + "::")

            ]

            for key in remove_keys:

                self._cache.pop(key, None)

    # ======================================================
    # Clear Complete Cache
    # ======================================================

    def clear_all(self) -> None:

        with self._lock:

            self._cache.clear()

    # ======================================================
    # Cache Statistics
    # ======================================================

    def cache_size(self) -> int:

        return len(self._cache)

    def cache_symbols(self) -> list[str]:

        symbols = set()

        for entry in self._cache.values():

            symbols.add(entry.symbol)

        return sorted(symbols)

    def cache_intervals(self) -> list[str]:

        intervals = set()

        for entry in self._cache.values():

            intervals.add(entry.interval)

        return sorted(intervals)

    def cache_info(self) -> dict:

        info = {}

        with self._lock:

            for key, entry in self._cache.items():

                ttl = self.CACHE_SECONDS.get(

                    entry.interval,

                    300,

                )

                age = time.time() - entry.timestamp

                info[key] = {

                    "symbol": entry.symbol,

                    "interval": entry.interval,

                    "rows": len(entry.dataframe),

                    "age_seconds": round(age, 2),

                    "ttl_seconds": ttl,

                    "valid": age < ttl,

                }

        return info

    # ======================================================
    # Latest Quote
    # ======================================================

    def latest_price(

        self,

        symbol: str,

        interval: str = "1d",

    ) -> Optional[float]:

        df = self.get_ohlc(

            symbol=symbol,

            interval=interval,

        )

        if df.empty:

            return None

        try:

            return float(df["close"].iloc[-1])

        except Exception:

            return None

    # ======================================================
    # Latest Volume
    # ======================================================

    def latest_volume(

        self,

        symbol: str,

        interval: str = "1d",

    ) -> Optional[int]:

        df = self.get_ohlc(

            symbol=symbol,

            interval=interval,

        )

        if df.empty:

            return None

        try:

            return int(df["volume"].iloc[-1])

        except Exception:

            return None

    # ======================================================
    # Has Cache
    # ======================================================

    def has_cache(

        self,

        symbol: str,

        interval: str = "1d",

    ) -> bool:

        key = self._cache_key(symbol, interval)

        return self._is_valid(key)

    # ======================================================
    # Get Cached Data
    # ======================================================

    def get_cached(

        self,

        symbol: str,

        interval: str = "1d",

    ) -> Optional[pd.DataFrame]:

        key = self._cache_key(symbol, interval)

        if not self._is_valid(key):

            return None

        return self._cache[key].dataframe


# ==========================================================
# Singleton Instance
# ==========================================================

market_data_hub = MarketDataHub()