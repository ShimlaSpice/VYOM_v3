"""
Sprint 53
Incremental Refresh Engine
"""

from __future__ import annotations

import threading
import time


class RefreshEngine:

    def __init__(self):

        self._timestamps: dict[str, float] = {}

        self._lock = threading.Lock()

    def mark(

        self,

        symbol: str,

    ):

        with self._lock:

            self._timestamps[symbol] = time.time()

    def last_refresh(

        self,

        symbol: str,

    ) -> float:

        return self._timestamps.get(

            symbol,

            0.0,

        )

    def needs_refresh(

        self,

        symbol: str,

        seconds: int = 60,

    ) -> bool:

        return (

            time.time()

            - self.last_refresh(

                symbol,

            )

        ) >= seconds

    def refresh(

        self,

        provider,

        symbol: str,

    ):

        provider.get_market_context(

            symbol,

        )

        self.mark(

            symbol,

        )

    def refresh_many(

        self,

        provider,

        symbols: list[str],

    ):

        for symbol in symbols:

            try:

                self.refresh(

                    provider,

                    symbol,

                )

            except Exception:

                pass

    def clear(self):

        self._timestamps.clear()


refresh_engine = RefreshEngine()