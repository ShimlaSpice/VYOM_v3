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

        self.mapping = {

            "nifty50": "nifty50.txt",

            "nifty100": "nifty100.txt",

            "nifty200": "nifty200.txt",

            "nifty500": "nifty500.txt",

            "next50": "next50.txt",

            "banknifty": "banknifty.txt",

            "fo": "fo.txt",

            "midcap": "midcap.txt",

            "smallcap": "smallcap.txt",

            "microcap": "microcap.txt",

            "penny": "penny.txt",

            "sme": "sme.txt",

            "etf": "etf.txt",

            "reit": "reit.txt",

            "invit": "invit.txt",

            "auto": "auto.txt",

            "bank": "bank.txt",

            "it": "it.txt",

            "pharma": "pharma.txt",

            "fmcg": "fmcg.txt",

            "realty": "realty.txt",

            "energy": "energy.txt",

            "metal": "metal.txt",

            "psu": "psu.txt",

            "defence": "defence.txt",

            "chemical": "chemical.txt",

            "textile": "textile.txt",

            "media": "media.txt",

            "telecom": "telecom.txt",

            "healthcare": "healthcare.txt",

            "capitalgoods": "capitalgoods.txt",

            "financial": "financial.txt",

            "all": "all.txt",

            "custom": "custom.txt",

        }

    def get_symbols(

        self,

        universe: str,

    ) -> list[str]:

        filename = self.mapping.get(

            universe.lower(),

        )

        if filename is None:

            return []

        file = self.base_path / filename

        if not file.exists():

            return []

        with open(

            file,

            "r",

            encoding="utf-8",

        ) as f:

            symbols = [

                line.strip()

                for line in f

                if line.strip()

            ]

        return sorted(

            list(

                dict.fromkeys(

                    symbols,

                )

            )

        )

    def available_universes(

        self,

    ) -> list[str]:

        return sorted(

            self.mapping.keys()

        )