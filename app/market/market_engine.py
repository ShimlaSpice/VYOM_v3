"""
Market Engine for VYOM.
"""

from __future__ import annotations

from app.market import MarketDataProvider


class MarketEngine:
    """
    Coordinates market data operations.
    """

    def __init__(self, provider: MarketDataProvider):
        self.provider = provider

    def load_history(
        self,
        symbol: str,
        interval: str = "1d",
        limit: int = 100,
    ):
        """
        Load historical candle data.
        """

        return self.provider.get_candles(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

    def load_quote(
        self,
        symbol: str,
    ):
        """
        Load current market quote.
        """

        return self.provider.get_quote(symbol)