"""
Market Data Provider Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MarketDataProvider(ABC):
    """
    Base class for every market data provider.
    """

    @abstractmethod
    def connect(self) -> None:
        """Connect to data source."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect."""

    @abstractmethod
    def get_quote(self, symbol: str) -> dict[str, Any]:
        """Return latest quote."""

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Return historical candles."""

    @abstractmethod
    def get_watchlist(self) -> list[str]:
        """Return symbols to scan."""