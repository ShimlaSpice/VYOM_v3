"""
Global Market Data Provider.

Downloads major global market indices.
"""

from __future__ import annotations

from typing import Any

import yfinance as yf


class GlobalMarketProvider:

    SYMBOLS = {

        "dow": "^DJI",

        "nasdaq": "^IXIC",

        "sp500": "^GSPC",

        "gift_nifty": "^NSEI",

        "crude": "CL=F",

        "gold": "GC=F",

        "usd_inr": "INR=X",

        "vix": "^VIX",

    }

    def _change(

        self,

        symbol: str,

    ) -> float:

        try:

            history = yf.download(

                symbol,

                period="5d",

                interval="1d",

                progress=False,

                auto_adjust=False,

            )

            if len(history) < 2:

                return 0.0

            close = history["Close"]

            previous = float(close.iloc[-2])

            latest = float(close.iloc[-1])

            if previous == 0:

                return 0.0

            return round(

                ((latest - previous) / previous) * 100,

                2,

            )

        except Exception:

            return 0.0

    def fetch(

        self,

    ) -> dict[str, Any]:

        return {

            name: self._change(

                symbol,

            )

            for name, symbol in self.SYMBOLS.items()

        }