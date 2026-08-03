"""
Sector Mapper.
"""

from __future__ import annotations

import yfinance as yf


class SectorMapper:

    def get_sector(
        self,
        symbol: str,
    ) -> str:

        try:

            ticker = yf.Ticker(symbol)

            info = ticker.info

            return info.get(
                "sector",
                "Unknown",
            )

        except Exception:

            return "Unknown"