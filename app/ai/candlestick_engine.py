"""
Candlestick Pattern Engine for VYOM.

Detects common bullish and bearish candlestick patterns.
"""

from __future__ import annotations


class CandlestickEngine:

    def analyze(

        self,

        opens: list[float],

        highs: list[float],

        lows: list[float],

        closes: list[float],

    ) -> dict:

        if min(

            len(opens),

            len(highs),

            len(lows),

            len(closes),

        ) < 2:

            return {

                "pattern": "UNKNOWN",

                "signal": "NEUTRAL",

                "strength": 0,

                "reasons": [

                    "Insufficient candle data",

                ],

            }

        o1 = opens[-2]
        h1 = highs[-2]
        l1 = lows[-2]
        c1 = closes[-2]

        o2 = opens[-1]
        h2 = highs[-1]
        l2 = lows[-1]
        c2 = closes[-1]

        body = abs(

            c2 - o2,

        )

        candle_range = max(

            h2 - l2,

            0.000001,

        )

        upper_shadow = h2 - max(

            o2,

            c2,

        )

        lower_shadow = min(

            o2,

            c2,

        ) - l2

        pattern = "NONE"

        signal = "NEUTRAL"

        strength = 0

        reasons = []

        # ---------------------------------
        # Bullish Engulfing
        # ---------------------------------

        if (

            c1 < o1

            and c2 > o2

            and o2 <= c1

            and c2 >= o1

        ):

            pattern = "BULLISH_ENGULFING"

            signal = "BULLISH"

            strength = 9

            reasons.append(

                "Bullish Engulfing detected",

            )

        # ---------------------------------
        # Bearish Engulfing
        # ---------------------------------

        elif (

            c1 > o1

            and c2 < o2

            and o2 >= c1

            and c2 <= o1

        ):

            pattern = "BEARISH_ENGULFING"

            signal = "BEARISH"

            strength = 9

            reasons.append(

                "Bearish Engulfing detected",

            )

        # ---------------------------------
        # Hammer
        # ---------------------------------

        elif (

            lower_shadow > body * 2

            and upper_shadow < body

        ):

            pattern = "HAMMER"

            signal = "BULLISH"

            strength = 8

            reasons.append(

                "Hammer pattern detected",

            )

        # ---------------------------------
        # Shooting Star
        # ---------------------------------

        elif (

            upper_shadow > body * 2

            and lower_shadow < body

        ):

            pattern = "SHOOTING_STAR"

            signal = "BEARISH"

            strength = 8

            reasons.append(

                "Shooting Star detected",

            )

        # ---------------------------------
        # Doji
        # ---------------------------------

        elif (

            body / candle_range

        ) < 0.10:

            pattern = "DOJI"

            signal = "NEUTRAL"

            strength = 5

            reasons.append(

                "Market indecision (Doji)",

            )

        # ---------------------------------
        # Strong Bull Candle
        # ---------------------------------

        elif (

            c2 > o2

            and body / candle_range > 0.70

        ):

            pattern = "STRONG_BULL"

            signal = "BULLISH"

            strength = 7

            reasons.append(

                "Strong bullish candle",

            )

        # ---------------------------------
        # Strong Bear Candle
        # ---------------------------------

        elif (

            c2 < o2

            and body / candle_range > 0.70

        ):

            pattern = "STRONG_BEAR"

            signal = "BEARISH"

            strength = 7

            reasons.append(

                "Strong bearish candle",

            )

        else:

            reasons.append(

                "No major candlestick pattern",

            )

        return {

            "pattern": pattern,

            "signal": signal,

            "strength": strength,

            "reasons": reasons,

        }