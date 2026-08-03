"""
Watchlist Loader.
"""

from __future__ import annotations

from pathlib import Path


class WatchlistLoader:

    _CACHE: dict[str, list[str]] = {}

    def __init__(self):

        self.base_path = (

            Path(__file__)

            .resolve()

            .parents[2]

            / "data"

            / "watchlists"

        )

    def load(

        self,

        filename: str,

        limit: int | None = None,

    ) -> list[str]:

        filename = filename.lower()

        if filename in self._CACHE:

            symbols = self._CACHE[filename]

        else:

            path = self.base_path / filename

            if not path.exists():

                raise FileNotFoundError(

                    f"Watchlist file not found: {path}"

                )

            with open(

                path,

                "r",

                encoding="utf-8",

            ) as file:

                symbols = sorted(

                    list(

                        dict.fromkeys(

                            line.strip().upper()

                            for line in file

                            if line.strip()

                        )

                    )

                )

            self._CACHE[filename] = symbols

        if limit is None:

            return symbols

        return symbols[:limit]

    def preload(self):

        if not self.base_path.exists():

            return

        for file in self.base_path.glob("*.txt"):

            filename = file.name.lower()

            if filename in self._CACHE:

                continue

            try:

                self.load(

                    filename,

                )

            except Exception:

                continue

    def available(self):

        self.preload()

        return sorted(

            self._CACHE.keys()

        )

    def clear_cache(self):

        self._CACHE.clear()

    def cache_size(self):

        return len(

            self._CACHE,

        )