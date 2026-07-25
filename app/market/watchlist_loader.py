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

    def load(

        self,

        filename: str,

        limit: int | None = None,

    ) -> list[str]:

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

            symbols = [

                line.strip()

                for line in file

                if line.strip()

            ]

        if limit is not None:

            return symbols[:limit]

        return symbols