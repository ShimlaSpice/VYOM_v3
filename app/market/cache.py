"""
High Performance Market Cache.
"""

from __future__ import annotations

import time
from typing import Any


class MarketCache:

    CACHE_EXPIRY = 300

    def __init__(self):

        self._quotes: dict[str, tuple[float, dict[str, Any]]] = {}

        self._candles: dict[str, tuple[float, list[dict[str, Any]]]] = {}

        self._fundamentals: dict[str, tuple[float, dict[str, Any]]] = {}

    def _expired(

        self,

        timestamp: float,

    ) -> bool:

        return (

            time.time() - timestamp

        ) > self.CACHE_EXPIRY

    # ---------------- Quotes ----------------

    def get_quote(

        self,

        symbol: str,

    ):

        item = self._quotes.get(symbol)

        if item is None:

            return None

        ts, value = item

        if self._expired(ts):

            del self._quotes[symbol]

            return None

        return value

    def set_quote(

        self,

        symbol: str,

        quote: dict[str, Any],

    ) -> None:

        self._quotes[symbol] = (

            time.time(),

            quote,

        )

    # ---------------- Candles ----------------

    def get_candles(

        self,

        symbol: str,

    ):

        item = self._candles.get(symbol)

        if item is None:

            return None

        ts, value = item

        if self._expired(ts):

            del self._candles[symbol]

            return None

        return value

    def set_candles(

        self,

        symbol: str,

        candles: list[dict[str, Any]],

    ):

        self._candles[symbol] = (

            time.time(),

            candles,

        )

    # ---------------- Fundamentals ----------------

    def get_fundamentals(

        self,

        symbol: str,

    ):

        item = self._fundamentals.get(symbol)

        if item is None:

            return None

        ts, value = item

        if self._expired(ts):

            del self._fundamentals[symbol]

            return None

        return value

    def set_fundamentals(

        self,

        symbol: str,

        fundamentals: dict[str, Any],

    ):

        self._fundamentals[symbol] = (

            time.time(),

            fundamentals,

        )

    # ---------------- Utilities ----------------

    def clear(

        self,

    ):

        self._quotes.clear()

        self._candles.clear()

        self._fundamentals.clear()

    def statistics(

        self,

    ):

        return {

            "quotes": len(self._quotes),

            "candles": len(self._candles),

            "fundamentals": len(self._fundamentals),

        }