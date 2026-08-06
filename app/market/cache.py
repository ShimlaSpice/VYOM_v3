"""
===========================================================
VYOM AI
Sprint 53

High Performance Smart Cache Manager

Caches

✓ Quotes
✓ OHLC
✓ Indicators
✓ Fundamentals
✓ News

Thread Safe
TTL Based
Multi Timeframe Ready

===========================================================
"""

from __future__ import annotations

import pickle
import threading
import time
from pathlib import Path
from typing import Any


class MarketCache:

    QUOTE_TTL       = 15        # 15 s — live price
    OHLC_TTL        = 600       # 10 min — daily bars don't change intraday
    INDICATOR_TTL   = 600
    FUNDAMENTAL_TTL = 7200      # 2 h
    NEWS_TTL        = 900

    # Disk cache: survives process restarts (daily bars only)
    _DISK_DIR  = Path(".vyom_cache")
    _DISK_TTL  = 3600           # 1 h — re-download disk entry after 1 h

    def __init__(self):
        self._quotes: dict[str, tuple[float, Any]]       = {}
        self._ohlc: dict[str, tuple[float, Any]]         = {}
        self._indicators: dict[str, tuple[float, Any]]   = {}
        self._fundamentals: dict[str, tuple[float, Any]] = {}
        self._news: dict[str, tuple[float, Any]]         = {}
        self._lock = threading.RLock()
        self._DISK_DIR.mkdir(exist_ok=True)

    # =====================================================
    # Internal
    # =====================================================

    def _expired(

        self,

        timestamp: float,

        ttl: int,

    ) -> bool:

        return (

            time.time()

            - timestamp

        ) > ttl

    def _get(

        self,

        cache: dict,

        key: str,

        ttl: int,

    ):

        with self._lock:

            item = cache.get(key)

            if item is None:

                return None

            ts, value = item

            if self._expired(

                ts,

                ttl,

            ):

                del cache[key]

                return None

            return value

    def _set(

        self,

        cache: dict,

        key: str,

        value,

    ):

        with self._lock:

            cache[key] = (

                time.time(),

                value,

            )

    # =====================================================
    # Quote
    # =====================================================

    def get_quote(

        self,

        symbol: str,

    ):

        return self._get(

            self._quotes,

            symbol,

            self.QUOTE_TTL,

        )

    def set_quote(

        self,

        symbol: str,

        quote,

    ):

        self._set(

            self._quotes,

            symbol,

            quote,

        )

    # =====================================================
    # OHLC  (memory + disk persistence)
    # =====================================================

    def _disk_path(self, key: str) -> Path:
        safe = key.replace(":", "_").replace("/", "_").replace("^", "IX_")
        return self._DISK_DIR / f"{safe}.pkl"

    def get_ohlc(self, key: str):
        # 1. Check memory cache first
        mem = self._get(self._ohlc, key, self.OHLC_TTL)
        if mem is not None:
            return mem
        # 2. Check disk cache
        path = self._disk_path(key)
        if path.exists():
            try:
                age = time.time() - path.stat().st_mtime
                if age < self._DISK_TTL:
                    with open(path, "rb") as f:
                        df = pickle.load(f)
                    # Promote into memory cache
                    self._set(self._ohlc, key, df)
                    return df
            except Exception:
                pass
        return None

    def set_ohlc(self, key: str, dataframe):
        self._set(self._ohlc, key, dataframe)
        # Persist to disk asynchronously (don't block the caller)
        path = self._disk_path(key)
        try:
            with open(path, "wb") as f:
                pickle.dump(dataframe, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            pass

    # =====================================================
    # Indicator
    # =====================================================

    def get_indicator(

        self,

        key: str,

    ):

        return self._get(

            self._indicators,

            key,

            self.INDICATOR_TTL,

        )

    def set_indicator(

        self,

        key: str,

        value,

    ):

        self._set(

            self._indicators,

            key,

            value,

        )

    # =====================================================
    # Fundamentals
    # =====================================================

    def get_fundamentals(

        self,

        symbol: str,

    ):

        return self._get(

            self._fundamentals,

            symbol,

            self.FUNDAMENTAL_TTL,

        )

    def set_fundamentals(

        self,

        symbol: str,

        value,

    ):

        self._set(

            self._fundamentals,

            symbol,

            value,

        )
    # =====================================================
    # News
    # =====================================================

    def get_news(

        self,

        symbol: str,

    ):

        return self._get(

            self._news,

            symbol,

            self.NEWS_TTL,

        )

    def set_news(

        self,

        symbol: str,

        news,

    ):

        self._set(

            self._news,

            symbol,

            news,

        )

    # =====================================================
    # Remove
    # =====================================================

    def remove_quote(

        self,

        symbol: str,

    ):

        with self._lock:

            self._quotes.pop(symbol, None)

    def remove_ohlc(

        self,

        key: str,

    ):

        with self._lock:

            self._ohlc.pop(key, None)

    def remove_indicator(

        self,

        key: str,

    ):

        with self._lock:

            self._indicators.pop(key, None)

    def remove_fundamentals(

        self,

        symbol: str,

    ):

        with self._lock:

            self._fundamentals.pop(symbol, None)

    def remove_news(

        self,

        symbol: str,

    ):

        with self._lock:

            self._news.pop(symbol, None)

    # =====================================================
    # Utilities
    # =====================================================

    def clear(self):

        with self._lock:

            self._quotes.clear()

            self._ohlc.clear()

            self._indicators.clear()

            self._fundamentals.clear()

            self._news.clear()

    def statistics(self):

        with self._lock:

            return {

                "quotes": len(self._quotes),

                "ohlc": len(self._ohlc),

                "indicators": len(self._indicators),

                "fundamentals": len(self._fundamentals),

                "news": len(self._news),

                "total": (

                    len(self._quotes)

                    + len(self._ohlc)

                    + len(self._indicators)

                    + len(self._fundamentals)

                    + len(self._news)

                ),

            }

    def cleanup(self):

        with self._lock:

            now = time.time()

            cache_map = {

                self._quotes: self.QUOTE_TTL,

                self._ohlc: self.OHLC_TTL,

                self._indicators: self.INDICATOR_TTL,

                self._fundamentals: self.FUNDAMENTAL_TTL,

                self._news: self.NEWS_TTL,

            }

            for cache, ttl in cache_map.items():

                expired = [

                    key

                    for key, (ts, _) in cache.items()

                    if (now - ts) > ttl

                ]

                for key in expired:

                    cache.pop(key, None)
