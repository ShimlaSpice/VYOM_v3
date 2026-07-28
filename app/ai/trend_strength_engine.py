"""
Trend Strength Engine for VYOM.

Uses ADX to determine whether the market is
trending or ranging.
"""

from __future__ import annotations


class TrendStrengthEngine:

    def analyze(

        self,

        highs: list[float],

        lows: list[float],

        closes: list[float],

        period: int = 14,

    ) -> dict:

        if (

            len(highs) < period + 1

            or len(lows) < period + 1

            or len(closes) < period + 1

        ):

            return {

                "adx": 0.0,

                "trend": "UNKNOWN",

                "strength": "UNKNOWN",

                "score": 0,

                "reasons": [

                    "Insufficient price history",

                ],

            }

        plus_dm = []
        minus_dm = []
        true_range = []

        for i in range(1, len(closes)):

            up_move = highs[i] - highs[i - 1]
            down_move = lows[i - 1] - lows[i]

            plus_dm.append(

                up_move if (

                    up_move > down_move

                    and up_move > 0

                ) else 0

            )

            minus_dm.append(

                down_move if (

                    down_move > up_move

                    and down_move > 0

                ) else 0

            )

            tr = max(

                highs[i] - lows[i],

                abs(

                    highs[i] - closes[i - 1],

                ),

                abs(

                    lows[i] - closes[i - 1],

                ),

            )

            true_range.append(tr)

        atr = sum(

            true_range[-period:]

        ) / period

        if atr == 0:

            return {

                "adx": 0.0,

                "trend": "RANGE",

                "strength": "VERY WEAK",

                "score": 0,

                "reasons": [

                    "ATR is zero",

                ],

            }

        plus_di = (

            sum(

                plus_dm[-period:]

            ) / period

        ) / atr * 100

        minus_di = (

            sum(

                minus_dm[-period:]

            ) / period

        ) / atr * 100

        if plus_di + minus_di == 0:

            dx = 0

        else:

            dx = (

                abs(

                    plus_di - minus_di,

                )

                / (

                    plus_di + minus_di

                )

            ) * 100

        adx = round(

            dx,

            2,

        )

        if adx >= 50:

            strength = "VERY STRONG"
            score = 10

        elif adx >= 35:

            strength = "STRONG"
            score = 8

        elif adx >= 25:

            strength = "MODERATE"
            score = 6

        elif adx >= 20:

            strength = "WEAK"
            score = 4

        else:

            strength = "RANGE"
            score = 2

        if plus_di > minus_di:

            trend = "UPTREND"

        elif minus_di > plus_di:

            trend = "DOWNTREND"

        else:

            trend = "SIDEWAYS"

        reasons = [

            f"ADX = {adx:.2f}",

            f"+DI = {plus_di:.2f}",

            f"-DI = {minus_di:.2f}",

            f"{strength} {trend}",

        ]

        return {

            "adx": adx,

            "trend": trend,

            "strength": strength,

            "score": score,

            "plus_di": round(

                plus_di,

                2,

            ),

            "minus_di": round(

                minus_di,

                2,

            ),

            "reasons": reasons,

        }