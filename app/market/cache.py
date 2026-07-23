"""
Simple in-memory market cache.
"""

from __future__ import annotations

from typing import Any


class MarketCache:
    """
    Stores market data in memory during runtime.
    """

    def __init__(self) -> None:
        self._quotes: dict[str, dict[str, Any]] = {}
        self._candles: dict[str, list[dict[str, Any]]] = {}

    def get_quote(self, symbol: str):
        return self._quotes.get(symbol)

    def set_quote(
        self,
        symbol: str,
        quote: dict[str, Any],
    ) -> None:
        self._quotes[symbol] = quote

    def get_candles(self, symbol: str):
        return self._candles.get(symbol)

    def set_candles(
        self,
        symbol: str,
        candles: list[dict[str, Any]],
    ) -> None:
        self._candles[symbol] = candles

    def clear(self) -> None:
        self._quotes.clear()
        self._candles.clear()