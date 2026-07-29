"""
Market Data Provider Interface for VYOM.

Every market data source must implement this interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class MarketDataProvider(ABC):
    """
    Base interface for all market data providers.
    """

    @abstractmethod
    def connect(
        self,
    ) -> None:
        """
        Connect to provider.
        """

    @abstractmethod
    def disconnect(
        self,
    ) -> None:
        """
        Disconnect provider.
        """

    @abstractmethod
    def get_quote(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Latest quote for a symbol.
        """

    @abstractmethod
    def get_bulk_quotes(
        self,
        symbols: list[str],
    ) -> dict[str, Any]:
        """
        Latest quotes for multiple symbols.
        """

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Historical OHLCV candles.
        """

    @abstractmethod
    def prefetch(
        self,
        symbols: list[str],
        period: str = "3mo",
        interval: str = "1d",
    ) -> None:
        """
        Batch download market data.
        """

    @abstractmethod
    def get_fundamentals(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Company fundamentals.
        """

    @abstractmethod
    def get_news(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Latest company news.
        """

    @abstractmethod
    def get_watchlist(
        self,
        universe: str = "nifty50",
    ) -> list[str]:
        """
        Symbols belonging to a universe.
        """

    @abstractmethod
    def get_market_status(
        self,
    ) -> dict[str, Any]:
        """
        Market open / closed / holiday.
        """

    @abstractmethod
    def get_indices(
        self,
    ) -> dict[str, Any]:
        """
        NIFTY, BANKNIFTY, SENSEX etc.
        """

    @abstractmethod
    def get_sector_data(
        self,
    ) -> dict[str, Any]:
        """
        Sector performance.
        """

    @abstractmethod
    def get_fii_dii_data(
        self,
    ) -> dict[str, Any]:
        """
        Latest FII/DII activity.
        """

    @abstractmethod
    def get_corporate_actions(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Dividends, bonus, split, rights etc.
        """

    @abstractmethod
    def get_insider_trades(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Insider buying / selling.
        """

    @abstractmethod
    def get_market_breadth(
        self,
    ) -> dict[str, Any]:
        """
        Advance / Decline statistics.
        """