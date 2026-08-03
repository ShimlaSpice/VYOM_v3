"""
Sector Strength Engine.
"""

from __future__ import annotations

from app.market import MarketDataProvider
from app.scanner.technical_indicators import TechnicalIndicators


class SectorEngine:

    SECTORS = {
        "BANK": "^NSEBANK",
        "IT": "^CNXIT",
        "AUTO": "^CNXAUTO",
        "FMCG": "^CNXFMCG",
        "PHARMA": "^CNXPHARMA",
    }

    def __init__(self, provider: MarketDataProvider):

        self.provider = provider

    def analyze(self) -> list[dict]:

        sectors = []

        for name, symbol in self.SECTORS.items():

            candles = self.provider.get_candles(
                symbol=symbol,
                interval="1d",
                limit=20,
            )

            if len(candles) < 2:
                continue

            closes = [c["close"] for c in candles]

            change = TechnicalIndicators.price_change(
                closes[-1],
                closes[-2],
            )

            sectors.append(
                {
                    "sector": name,
                    "change": round(change, 2),
                }
            )

        sectors.sort(
            key=lambda x: x["change"],
            reverse=True,
        )

        return sectors