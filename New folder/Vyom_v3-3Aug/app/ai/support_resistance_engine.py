"""
Support & Resistance Engine for VYOM.
"""

from __future__ import annotations


class SupportResistanceEngine:

    def analyze(

        self,

        highs: list[float],

        lows: list[float],

        closes: list[float],

        lookback: int = 20,

    ) -> dict:

        if (

            len(highs) < lookback

            or len(lows) < lookback

            or not closes

        ):

            return {

                "support": 0.0,

                "resistance": 0.0,

                "distance_to_support": 0.0,

                "distance_to_resistance": 0.0,

                "position": "UNKNOWN",

            }

        support = min(

            lows[-lookback:]

        )

        resistance = max(

            highs[-lookback:]

        )

        current = closes[-1]

        distance_to_support = round(

            ((current - support) / current) * 100,

            2,

        )

        distance_to_resistance = round(

            ((resistance - current) / current) * 100,

            2,

        )

        if current >= resistance:

            position = "BREAKOUT"

        elif distance_to_resistance < 2:

            position = "NEAR_RESISTANCE"

        elif distance_to_support < 2:

            position = "NEAR_SUPPORT"

        else:

            position = "RANGE"

        return {

            "support": round(

                support,

                2,

            ),

            "resistance": round(

                resistance,

                2,

            ),

            "distance_to_support": distance_to_support,

            "distance_to_resistance": distance_to_resistance,

            "position": position,

        }
    