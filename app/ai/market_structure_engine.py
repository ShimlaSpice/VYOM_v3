"""
Market Structure Engine for VYOM.

Detects market structure using swing highs
and swing lows.

Jarvis should understand:

HH = Higher High
HL = Higher Low
LH = Lower High
LL = Lower Low

These define the market trend better than
indicators alone.
"""

from __future__ import annotations


class MarketStructureEngine:

    def analyze(

        self,

        highs: list[float],

        lows: list[float],

        lookback: int = 20,

    ) -> dict:

        if (

            len(highs) < lookback

            or len(lows) < lookback

        ):

            return {

                "trend": "UNKNOWN",

                "structure": "UNKNOWN",

                "score": 0,

                "reasons": [

                    "Insufficient data",

                ],

            }

        highs = highs[-lookback:]

        lows = lows[-lookback:]

        hh = 0
        hl = 0
        lh = 0
        ll = 0

        for i in range(1, len(highs)):

            if highs[i] > highs[i - 1]:

                hh += 1

            else:

                lh += 1

            if lows[i] > lows[i - 1]:

                hl += 1

            else:

                ll += 1

        # ---------------------------------

        if hh >= lh and hl >= ll:

            trend = "UPTREND"

            structure = "HH-HL"

            score = 10

            reasons = [

                "Higher Highs confirmed",

                "Higher Lows confirmed",

            ]

        elif lh > hh and ll > hl:

            trend = "DOWNTREND"

            structure = "LH-LL"

            score = 2

            reasons = [

                "Lower Highs confirmed",

                "Lower Lows confirmed",

            ]

        elif hh > lh:

            trend = "WEAK_UPTREND"

            structure = "MIXED"

            score = 7

            reasons = [

                "Higher Highs",

                "Mixed Lows",

            ]

        elif ll > hl:

            trend = "WEAK_DOWNTREND"

            structure = "MIXED"

            score = 4

            reasons = [

                "Lower Lows",

                "Mixed Highs",

            ]

        else:

            trend = "SIDEWAYS"

            structure = "RANGE"

            score = 5

            reasons = [

                "No clear market structure",

            ]

        return {

            "trend": trend,

            "structure": structure,

            "score": score,

            "higher_highs": hh,

            "higher_lows": hl,

            "lower_highs": lh,

            "lower_lows": ll,

            "reasons": reasons,

        }