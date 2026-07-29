"""
Universe Downloader.

Downloads and stores market universes.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class UniverseDownloader:

    BASE_URL = (
        "https://archives.nseindia.com/content/indices/"
    )

    FILES = {

        "NIFTY50":
        "ind_nifty50list.csv",

        "NIFTY100":
        "ind_nifty100list.csv",

        "NIFTY200":
        "ind_nifty200list.csv",

        "NIFTY500":
        "ind_nifty500list.csv",

    }

    def __init__(self):

        self.output = (

            Path(__file__).resolve().parents[2]

            / "data"

            / "watchlists"

        )

        self.output.mkdir(

            parents=True,

            exist_ok=True,

        )

    def download_all(self):

        for universe, filename in self.FILES.items():

            self.download(

                universe,

                filename,

            )

    def download(

        self,

        universe: str,

        filename: str,

    ):

        url = self.BASE_URL + filename

        dataframe = pd.read_csv(

            url,

        )

        symbols = (

            dataframe["Symbol"]

            .astype(str)

            .str.strip()

            + ".NS"

        )

        output_file = (

            self.output

            / f"{universe.lower()}.txt"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8",

        ) as file:

            file.write(

                "\n".join(

                    symbols.tolist()

                )

            )

        print(

            f"{universe} : {len(symbols)} symbols saved."

        )