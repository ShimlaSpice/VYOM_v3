"""
Trade Setup Generator for VYOM.
"""

from __future__ import annotations

import math

from app.trade_intelligence.atr_engine import ATREngine


class SetupGenerator:

    def __init__(self):

        self.atr_engine = ATREngine()

    def generate(

        self,

        highs: list[float],

        lows: list[float],

        closes: list[float],

        category: str,

    ) -> dict:

        if (

            not highs

            or not lows

            or not closes

        ):

            return self._empty()

        current_price = closes[-1]

        atr = self.atr_engine.calculate(

            highs,

            lows,

            closes,

        )

        if (

            current_price <= 0

            or math.isnan(current_price)

            or math.isnan(atr)

            or atr <= 0

        ):

            return self._empty()

        multipliers = {

            "INTRADAY": (1.0, 1.5, 2.0),

            "SWING": (1.5, 3.0, 5.0),

            "POSITIONAL": (2.0, 5.0, 8.0),

            "WATCH": (1.0, 1.0, 1.5),

            "AVOID": (1.0, 0.5, 1.0),

        }

        sl_multiplier, t1_multiplier, t2_multiplier = multipliers.get(

            category,

            multipliers["AVOID"],

        )

        entry = current_price

        stop_loss = entry - (atr * sl_multiplier)

        target1 = entry + (atr * t1_multiplier)

        target2 = entry + (atr * t2_multiplier)

        risk = max(

            entry - stop_loss,

            0.01,

        )

        reward = max(

            target1 - entry,

            0.0,

        )

        risk_reward = round(

            reward / risk,

            2,

        )

        return {

            "entry": round(

                entry,

                2,

            ),

            "stop_loss": round(

                stop_loss,

                2,

            ),

            "target1": round(

                target1,

                2,

            ),

            "target2": round(

                target2,

                2,

            ),

            "risk_reward": risk_reward,

            "atr": round(

                atr,

                2,

            ),

            "trade": category != "AVOID",

        }

    def _empty(

        self,

    ) -> dict:

        return {

            "entry": 0.0,

            "stop_loss": 0.0,

            "target1": 0.0,

            "target2": 0.0,

            "risk_reward": 0.0,

            "atr": 0.0,

            "trade": False,

        }