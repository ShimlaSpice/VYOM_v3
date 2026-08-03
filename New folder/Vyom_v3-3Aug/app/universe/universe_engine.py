"""
Universe Engine.
"""

from __future__ import annotations

from app.universe.universe_manager import UniverseManager


class UniverseEngine:

    _CACHE: dict[str, list[str]] = {}

    def __init__(self):

        self.manager = UniverseManager()

    def get_universe(

        self,

        universe: str = "NIFTY50",

    ) -> list[str]:

        key = universe.lower()

        if key in self._CACHE:

            return self._CACHE[key]

        symbols = self.manager.get_symbols(

            key,

        )

        if not symbols:

            fallback = self.manager.get_symbols(

                "nifty50",

            )

            self._CACHE[key] = fallback

            return fallback

        self._CACHE[key] = symbols

        return symbols

    def available_universes(

        self,

    ) -> list[str]:

        return [

            item.upper()

            for item in self.manager.available_universes()

        ]

    def clear_cache(

        self,

    ):

        self._CACHE.clear()

    def reload(

        self,

    ):

        self.clear_cache()