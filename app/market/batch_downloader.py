"""
Batch Market Downloader.
"""

from __future__ import annotations

import yfinance as yf


class BatchDownloader:

    def download(

        self,

        symbols: list[str],

        period: str = "3mo",

        interval: str = "1d",

    ):

        return yf.download(

            tickers=symbols,

            period=period,

            interval=interval,

            group_by="ticker",

            threads=True,

            progress=False,

            auto_adjust=False,

        )