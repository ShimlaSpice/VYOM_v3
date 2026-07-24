"""
Fundamental Analysis Engine.
"""

from __future__ import annotations

import yfinance as yf


class FundamentalEngine:

    def analyze(
        self,
        symbol: str,
    ) -> dict:

        ticker = yf.Ticker(symbol)

        info = ticker.info

        return {

            "symbol": symbol,

            "company": info.get(
                "longName",
                ""
            ),

            "sector": info.get(
                "sector",
                ""
            ),

            "market_cap": info.get(
                "marketCap",
                0,
            ),

            "pe": info.get(
                "trailingPE",
                0,
            ),

            "eps": info.get(
                "trailingEps",
                0,
            ),

            "dividend_yield": info.get(
                "dividendYield",
                0,
            ),

            "roe": info.get(
                "returnOnEquity",
                None,
            ),

            "debt_to_equity": info.get(
                "debtToEquity",
                None,
            ),
        }