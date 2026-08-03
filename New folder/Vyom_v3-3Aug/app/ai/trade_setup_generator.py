"""
Trade Setup Generator.
"""

from __future__ import annotations

from core.market_context import MarketContext


class TradeSetupGenerator:

    def generate(
        self,
        context: MarketContext,
    ) -> dict:

        indicators = context.indicators

        entry = context.close

        atr = indicators["atr"]

        stop_loss = round(
            entry - (atr * 1.5),
            2,
        )

        target1 = round(
            entry + (atr * 2),
            2,
        )

        target2 = round(
            entry + (atr * 4),
            2,
        )

        risk = max(
            entry - stop_loss,
            0.01,
        )

        reward = target2 - entry

        risk_reward = round(
            reward / risk,
            2,
        )

        if risk_reward >= 3:
            quality = "EXCELLENT"

        elif risk_reward >= 2:
            quality = "GOOD"

        elif risk_reward >= 1.5:
            quality = "AVERAGE"

        else:
            quality = "POOR"

        return {

            "entry": round(entry, 2),

            "stop_loss": stop_loss,

            "target1": target1,

            "target2": target2,

            "exit_price": target2,

            "risk_reward": risk_reward,

            "quality": quality,

            "atr": atr,

            "volatility": indicators["volatility"],

            "trend": indicators["trend"],

        }