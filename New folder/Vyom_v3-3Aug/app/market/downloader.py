"""
High Performance Batch Downloader
Sprint 53A
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from app.market.market_data_provider import MarketDataProvider


class BatchDownloader:

    MAX_WORKERS = 16

    def __init__(

        self,

        provider: MarketDataProvider,

    ):

        self.provider = provider

    def _download(

        self,

        symbol: str,

        interval: str,

        limit: int,

    ):

        try:

            return (

                symbol,

                self.provider.get_candles(

                    symbol=symbol,

                    interval=interval,

                    limit=limit,

                ),

            )

        except Exception:

            return (

                symbol,

                [],

            )

    def download_history(

        self,

        symbols: list[str],

        interval: str = "1d",

        limit: int = 100,

    ) -> dict[str, list[dict[str, Any]]]:

        start = time.perf_counter()

        symbols = sorted(

            set(symbols),

        )

        results = {}

        with ThreadPoolExecutor(

            max_workers=min(

                self.MAX_WORKERS,

                len(symbols),

            ),

        ) as executor:

            futures = [

                executor.submit(

                    self._download,

                    symbol,

                    interval,

                    limit,

                )

                for symbol in symbols

            ]

            for future in futures:

                symbol, candles = future.result()

                results[symbol] = candles

        elapsed = time.perf_counter() - start

        print()

        print("=" * 60)

        print("Batch Download Summary")

        print("=" * 60)

        print(f"Symbols     : {len(symbols)}")

        print(f"Downloaded  : {len(results)}")

        print(f"Time Taken  : {elapsed:.2f} sec")

        print("=" * 60)

        return results