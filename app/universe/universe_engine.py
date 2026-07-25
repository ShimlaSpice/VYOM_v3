"""
Universe Engine.

Provides stock universe for scanning.
"""

from __future__ import annotations

from app.market import YahooFinanceProvider


class UniverseEngine:

    def __init__(self):

        self.provider = YahooFinanceProvider()

    def get_universe(

        self,

        universe: str = "NIFTY50",

    ) -> list[str]:

        universe = universe.upper()

        if universe == "NIFTY50":

            return self.provider.get_watchlist()

        raise ValueError(
            f"Unknown universe: {universe}"
        )