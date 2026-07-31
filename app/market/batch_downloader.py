"""
===========================================================
VYOM AI
Sprint 53

High Performance Batch Downloader

Features
--------
✓ Bulk Yahoo Download
✓ Multi-Timeframe
✓ Smart Cache
✓ Duplicate Removal
✓ Thread Safe
✓ Connection Reuse
✓ Incremental Refresh Ready

===========================================================
"""

from __future__ import annotations

import threading
import time
from typing import Dict

import pandas as pd
import yfinance as yf


class BatchDownloader:

    CACHE_TTL = 300

    def __init__(self):

        self._cache: Dict[tuple, tuple[float, pd.DataFrame]] = {}

        self._lock = threading.RLock()

    # =====================================================
    # Cache
    # =====================================================

    def _expired(

        self,

        timestamp: float,

    ) -> bool:

        return (

            time.time()

            - timestamp

        ) > self.CACHE_TTL

    def _cache_key(

        self,

        symbols: list[str],

        period: str,

        interval: str,

    ) -> tuple:

        return (

            tuple(

                sorted(

                    set(

                        s.upper()

                        for s in symbols

                    )

                )

            ),

            period,

            interval,

        )

    # =====================================================
    # Download
    # =====================================================

    def download(

        self,

        symbols: list[str],

        period: str = "6mo",

        interval: str = "1d",

        refresh: bool = False,

    ) -> pd.DataFrame:

        if not symbols:

            return pd.DataFrame()

        key = self._cache_key(

            symbols,

            period,

            interval,

        )

        with self._lock:

            if (

                not refresh

                and key in self._cache

            ):

                ts, df = self._cache[key]

                if not self._expired(ts):

                    return df

            data = yf.download(

                tickers=list(key[0]),

                period=period,

                interval=interval,

                group_by="ticker",

                auto_adjust=False,

                threads=True,

                progress=False,

                prepost=False,

            )

            self._cache[key] = (

                time.time(),

                data,

            )

            return data

    # =====================================================
    # Single Symbol
    # =====================================================

    def download_symbol(

        self,

        symbol: str,

        period: str = "6mo",

        interval: str = "1d",

        refresh: bool = False,

    ) -> pd.DataFrame:

        return self.download(

            [symbol],

            period,

            interval,

            refresh,

        )

    # =====================================================
    # Multiple Timeframes
    # =====================================================

    def download_multi_timeframe(

        self,

        symbols: list[str],

        intervals: list[str],

        period: str = "6mo",

        refresh: bool = False,

    ) -> Dict[str, pd.DataFrame]:

        result: Dict[str, pd.DataFrame] = {}

        for interval in intervals:

            result[interval] = self.download(

                symbols=symbols,

                period=period,

                interval=interval,

                refresh=refresh,

            )

        return result

    # =====================================================
    # Incremental Refresh
    # =====================================================

    def refresh(

        self,

        symbols: list[str],

        period: str = "6mo",

        interval: str = "1d",

    ) -> pd.DataFrame:

        return self.download(

            symbols=symbols,

            period=period,

            interval=interval,

            refresh=True,

        )

    # =====================================================
    # Cache Utilities
    # =====================================================

    def clear_cache(self):

        with self._lock:

            self._cache.clear()

    def remove(

        self,

        symbols: list[str],

        period: str = "6mo",

        interval: str = "1d",

    ):

        key = self._cache_key(

            symbols,

            period,

            interval,

        )

        with self._lock:

            self._cache.pop(key, None)

    def cache_size(self) -> int:

        return len(self._cache)

    def cache_keys(self):

        return list(self._cache.keys())

    # =====================================================
    # Cleanup Expired Cache
    # =====================================================

    def cleanup(self):

        with self._lock:

            expired = []

            for key, (ts, _) in self._cache.items():

                if self._expired(ts):

                    expired.append(key)

            for key in expired:

                self._cache.pop(key, None)

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:

        with self._lock:

            return {

                "entries": len(self._cache),

                "ttl_seconds": self.CACHE_TTL,

                "cached_requests": list(self._cache.keys()),

            }


# =========================================================
# Singleton
# =========================================================

batch_downloader = BatchDownloader()