"""
High Performance Batch Downloader.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf


class BatchDownloader:

    def __init__(self):

        self.cache = {}

    def download(

        self,

        symbols: list[str],

        period: str = "3mo",

        interval: str = "1d",

        refresh: bool = False,

    ) -> pd.DataFrame:

        symbols = sorted(

            list(

                set(symbols),

            )

        )

        cache_key = (

            tuple(symbols),

            period,

            interval,

        )

        if (

            not refresh

            and cache_key in self.cache

        ):

            return self.cache[cache_key]

        data = yf.download(

            tickers=symbols,

            period=period,

            interval=interval,

            group_by="ticker",

            auto_adjust=False,

            threads=True,

            progress=False,

            prepost=False,

        )

        self.cache[cache_key] = data

        return data

    def clear_cache(

        self,

    ) -> None:

        self.cache.clear()

    def cache_size(

        self,

    ) -> int:

        return len(

            self.cache,

        )