"""
Universe Engine.

Provides stock universe for scanning.
"""

from __future__ import annotations

from app.universe.universe_manager import UniverseManager


class UniverseEngine:

    def __init__(self):

        self.manager = UniverseManager()

    def get_universe(

        self,

        universe: str = "NIFTY50",

    ) -> list[str]:

        symbols = self.manager.get_symbols(

            universe,

        )

        if not symbols:

            raise ValueError(

                f"No symbols found for universe: {universe}"

            )

        return symbols

    def available_universes(

        self,

    ) -> list[str]:

        return [

            "NIFTY50",

            "NIFTY100",

            "NIFTY200",

            "NIFTY500",

            "FO",

            "MIDCAP",

            "SMALLCAP",

            "PENNY",

        ]