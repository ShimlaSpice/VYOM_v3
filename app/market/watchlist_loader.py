"""
Watchlist Loader.
"""

from __future__ import annotations

from pathlib import Path


class WatchlistLoader:

    def __init__(self) -> None:
        self.base_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "data"
            / "watchlists"
        )

    def load(self, filename: str) -> list[str]:

        path = self.base_path / filename

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as file:
            return [
                line.strip()
                for line in file
                if line.strip()
            ]