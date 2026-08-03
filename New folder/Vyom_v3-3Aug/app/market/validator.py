"""
Market Data Validator.
"""

from __future__ import annotations

from typing import Any


class MarketDataValidator:
    """
    Cleans and validates downloaded market data.
    """

    @staticmethod
    def validate_candles(
        candles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        validated: list[dict[str, Any]] = []

        for candle in candles:

            required = (
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            )

            if not all(key in candle for key in required):
                continue

            if candle["volume"] <= 0:
                continue

            if candle["high"] < candle["low"]:
                continue

            validated.append(candle)

        return validated