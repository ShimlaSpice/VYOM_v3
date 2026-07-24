"""
Trade Setup Engine.
"""

from __future__ import annotations


class TradeSetupEngine:

    def generate(
        self,
        current_price: float,
    ) -> dict:

        entry = round(current_price, 2)

        stop_loss = round(
            current_price * 0.98,
            2,
        )

        target1 = round(
            current_price * 1.03,
            2,
        )

        target2 = round(
            current_price * 1.06,
            2,
        )

        risk = entry - stop_loss
        reward = target1 - entry

        rr = round(
            reward / risk,
            2,
        ) if risk else 0

        return {

            "entry": entry,

            "stop_loss": stop_loss,

            "target1": target1,

            "target2": target2,

            "risk_reward": rr,
        }