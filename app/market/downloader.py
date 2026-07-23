"""
Batch Downloader for VYOM.
"""

from __future__ import annotations

import time

from app.market.market_data_provider import MarketDataProvider


class BatchDownloader:
    """
    Downloads historical data for multiple symbols.
    """

    def __init__(self, provider: MarketDataProvider):
        self.provider = provider

    def download_history(
        self,
        symbols: list[str],
        interval: str = "1d",
        limit: int = 100,
    ) -> dict[str, list[dict]]:

        start = time.perf_counter()

        results: dict[str, list[dict]] = {}

        successful = 0
        failed = 0

        for symbol in symbols:

            try:

                candles = self.provider.get_candles(
                    symbol=symbol,
                    interval=interval,
                    limit=limit,
                )

                results[symbol] = candles

                successful += 1

            except Exception:

                results[symbol] = []

                failed += 1

        elapsed = time.perf_counter() - start

        print()
        print("=" * 60)
        print("Batch Download Summary")
        print("=" * 60)
        print(f"Symbols     : {len(symbols)}")
        print(f"Successful  : {successful}")
        print(f"Failed      : {failed}")
        print(f"Time Taken  : {elapsed:.2f} sec")
        print("=" * 60)

        return results