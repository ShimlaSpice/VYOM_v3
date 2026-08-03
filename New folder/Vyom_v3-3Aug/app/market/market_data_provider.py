"""
Market Data Provider Interface for VYOM.

Every market data source implements this interface. Kept intentionally
narrow (Interface Segregation): satellite concerns that already have
their own dedicated, working classes — sector data, FII/DII activity,
corporate actions, insider trades, global markets — are NOT part of
this contract. Compose those separately instead of forcing every
provider to stub methods it can't meaningfully implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.market_context import MarketContext


class MarketDataProvider(ABC):
    """Base interface for all market data providers."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to the provider."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect the provider."""

    @abstractmethod
    def get_quote(self, symbol: str) -> dict[str, Any]:
        """Latest quote for a symbol."""

    @abstractmethod
    def get_bulk_quotes(self, symbols: list[str]) -> dict[str, Any]:
        """Latest quotes for multiple symbols."""

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Historical OHLCV candles, most recent last."""

    @abstractmethod
    def get_market_context(self, symbol: str) -> MarketContext | None:
        """Full MarketContext (OHLCV + indicators + fundamentals + news)
        for a symbol, or None if not enough data is available. This is
        the primary entry point the Scanner and downstream engines use."""

    @abstractmethod
    def prefetch(
        self,
        symbols: list[str],
        period: str = "3mo",
        interval: str = "1d",
    ) -> None:
        """Batch-download and cache market data ahead of use."""

    @abstractmethod
    def get_fundamentals(self, symbol: str) -> dict[str, Any]:
        """Company fundamentals."""

    @abstractmethod
    def get_news(self, symbol: str) -> dict[str, Any]:
        """Latest company news."""

    @abstractmethod
    def get_watchlist(self, universe: str = "nifty50") -> list[str]:
        """Symbols belonging to a universe."""

    @abstractmethod
    def get_market_status(self) -> dict[str, Any]:
        """Market open / closed / holiday status."""