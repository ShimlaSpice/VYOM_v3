"""
Universe Manager.

Loads stock universes used by VYOM.
"""

from pathlib import Path


class UniverseManager:

    def __init__(self):

        self.base_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "watchlists"
        )

    def get_symbols(
        self,
        universe: str,
    ) -> list[str]:

        universe = universe.lower()

        mapping = {

            "nifty50": "nifty50.txt",
            "nifty100": "nifty100.txt",
            "nifty200": "nifty200.txt",
            "nifty500": "nifty500.txt",
            "fo": "fo.txt",
            "midcap": "midcap.txt",
            "smallcap": "smallcap.txt",
            "penny": "penny.txt",

        }

        filename = mapping.get(universe)

        if filename is None:
            raise ValueError(
                f"Unknown universe: {universe}"
            )

        file = self.base_path / filename

        if not file.exists():
            return []

        with open(
            file,
            "r",
            encoding="utf-8",
        ) as f:

            return [

                line.strip()

                for line in f

                if line.strip()

            ]