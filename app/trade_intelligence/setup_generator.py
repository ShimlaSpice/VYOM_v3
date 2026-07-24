"""
Trade Setup Generator for VYOM.
"""

from __future__ import annotations

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

        if not closes:

            return {}

        current_price = closes[-1]

        atr = self.atr_engine.calculate(

            highs,

            lows,

            closes,

        )

        # ------------------------------------------

        if category == "INTRADAY":

            sl_multiplier = 1

            t1_multiplier = 1.5

            t2_multiplier = 2

        elif category == "SWING":

            sl_multiplier = 1.5

            t1_multiplier = 3

            t2_multiplier = 5

        elif category == "POSITIONAL":

            sl_multiplier = 2

            t1_multiplier = 5

            t2_multiplier = 8

        elif category == "WATCH":

            sl_multiplier = 1

            t1_multiplier = 1

            t2_multiplier = 1.5

        else:

            sl_multiplier = 1

            t1_multiplier = 0.5

            t2_multiplier = 1

        entry = current_price

        stop_loss = current_price - (atr * sl_multiplier)

        target1 = current_price + (atr * t1_multiplier)

        target2 = current_price + (atr * t2_multiplier)

        risk = entry - stop_loss

        reward = target1 - entry

        rr = round(

            reward / risk,

            2,

        ) if risk else 0

        return {

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "target1": round(target1, 2),

            "target2": round(target2, 2),

            "risk_reward": rr,

            "atr": round(atr, 2),

            "trade": category != "AVOID",

        }