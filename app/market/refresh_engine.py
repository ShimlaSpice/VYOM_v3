"""
===========================================================
VYOM AI
Sprint 53

Refresh Engine

Responsibilities
----------------
✓ Incremental Refresh
✓ LTP Refresh
✓ OHLC Refresh
✓ Indicator Refresh
✓ Background Ready
✓ Cache Aware

===========================================================
"""

from __future__ import annotations

import threading
import time
from typing import Iterable

from app.market.market_data_hub import market_data_hub
from app.market.indicator_pipeline import indicator_pipeline


class RefreshEngine:

    DEFAULT_INTERVAL = "1d"

    DEFAULT_PERIOD = "6mo"

    def __init__(self):

        self._lock = threading.RLock()

        self._last_refresh = {}

    # =====================================================
    # Refresh Symbol
    # =====================================================

    def refresh_symbol(

        self,

        symbol: str,

        interval: str = DEFAULT_INTERVAL,

        period: str = DEFAULT_PERIOD,

    ):

        df = market_data_hub.refresh_symbol(

            symbol=symbol,

            interval=interval,

            period=period,

        )

        if df.empty:

            return df

        df = indicator_pipeline.process(df)

        self._last_refresh[

            (symbol, interval)

        ] = time.time()

        return df

    # =====================================================
    # Refresh Symbols
    # =====================================================

    def refresh_symbols(

        self,

        symbols: Iterable[str],

        interval: str = DEFAULT_INTERVAL,

        period: str = DEFAULT_PERIOD,

    ):

        result = {}

        for symbol in symbols:

            try:

                result[symbol] = self.refresh_symbol(

                    symbol,

                    interval,

                    period,

                )

            except Exception:

                continue

        return result

    # =====================================================
    # Refresh LTP Only
    # =====================================================

    def refresh_ltp(

        self,

        symbol: str,

        interval: str = DEFAULT_INTERVAL,

    ):

        df = market_data_hub.refresh_symbol(

            symbol=symbol,

            interval=interval,

        )

        if df.empty:

            return None

        return float(

            df["close"].iloc[-1]

        )

    # =====================================================
    # Refresh Indicators
    # =====================================================

    def refresh_indicators(

        self,

        symbol: str,

        interval: str = DEFAULT_INTERVAL,

    ):

        df = market_data_hub.get_ohlc(

            symbol,

            interval,

        )

        if df.empty:

            return df

        return indicator_pipeline.process(df)
    # =====================================================
    # Refresh Multiple Timeframes
    # =====================================================

    def refresh_multi_timeframe(

        self,

        symbol: str,

        intervals: list[str],

        period: str = DEFAULT_PERIOD,

    ):

        result = {}

        for interval in intervals:

            try:

                result[interval] = self.refresh_symbol(

                    symbol=symbol,

                    interval=interval,

                    period=period,

                )

            except Exception:

                continue

        return result

    # =====================================================
    # Last Refresh
    # =====================================================

    def last_refresh(

        self,

        symbol: str,

        interval: str = DEFAULT_INTERVAL,

    ):

        return self._last_refresh.get(

            (symbol, interval),

        )

    # =====================================================
    # Needs Refresh
    # =====================================================

    def needs_refresh(

        self,

        symbol: str,

        interval: str = DEFAULT_INTERVAL,

        seconds: int = 60,

    ) -> bool:

        last = self.last_refresh(

            symbol,

            interval,

        )

        if last is None:

            return True

        return (

            time.time()

            - last

        ) >= seconds

    # =====================================================
    # Background Refresh
    # =====================================================

    def background_refresh(

        self,

        symbols: Iterable[str],

        interval: str = DEFAULT_INTERVAL,

        period: str = DEFAULT_PERIOD,

    ):

        def worker():

            self.refresh_symbols(

                symbols=symbols,

                interval=interval,

                period=period,

            )

        thread = threading.Thread(

            target=worker,

            daemon=True,

        )

        thread.start()

        return thread

    # =====================================================
    # Refresh Status
    # =====================================================

    def status(self):

        return {

            "tracked_symbols": len(

                self._last_refresh

            ),

            "last_refresh": dict(

                self._last_refresh

            ),

        }

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        with self._lock:

            self._last_refresh.clear()


# =========================================================
# Singleton
# =========================================================

refresh_engine = RefreshEngine()