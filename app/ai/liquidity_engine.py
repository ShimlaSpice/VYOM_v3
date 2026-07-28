"""
Liquidity Engine for VYOM.

Evaluates whether a stock has sufficient liquidity
for safe trading.
"""

from __future__ import annotations


class LiquidityEngine:

    def analyze(

        self,

        current_volume: int,

        average_volume: float,

        delivery_percent: float | None = None,

        bid_price: float | None = None,

        ask_price: float | None = None,

    ) -> dict:

        score = 0

        reasons = []

        # -------------------------------------
        # Volume
        # -------------------------------------

        if average_volume <= 0:

            average_volume = 1

        volume_ratio = current_volume / average_volume

        if volume_ratio >= 3:

            score += 4

            reasons.append(

                "Exceptional Volume"

            )

        elif volume_ratio >= 2:

            score += 3

            reasons.append(

                "High Volume"

            )

        elif volume_ratio >= 1:

            score += 2

            reasons.append(

                "Healthy Volume"

            )

        else:

            score += 1

            reasons.append(

                "Low Volume"

            )

        # -------------------------------------
        # Delivery %
        # -------------------------------------

        if delivery_percent is not None:

            if delivery_percent >= 60:

                score += 3

                reasons.append(

                    "Strong Delivery Buying"

                )

            elif delivery_percent >= 40:

                score += 2

                reasons.append(

                    "Healthy Delivery"

                )

            else:

                score += 1

                reasons.append(

                    "Weak Delivery"

                )

        # -------------------------------------
        # Bid / Ask Spread
        # -------------------------------------

        spread = None

        if (

            bid_price is not None

            and ask_price is not None

            and bid_price > 0

            and ask_price > 0

        ):

            spread = (

                (ask_price - bid_price)

                / bid_price

            ) * 100

            if spread <= 0.10:

                score += 3

                reasons.append(

                    "Very Tight Spread"

                )

            elif spread <= 0.30:

                score += 2

                reasons.append(

                    "Healthy Spread"

                )

            elif spread <= 0.75:

                score += 1

                reasons.append(

                    "Acceptable Spread"

                )

            else:

                reasons.append(

                    "Wide Bid-Ask Spread"

                )

        # -------------------------------------
        # Final Rating
        # -------------------------------------

        if score >= 9:

            liquidity = "EXCELLENT"

        elif score >= 7:

            liquidity = "HIGH"

        elif score >= 5:

            liquidity = "MEDIUM"

        else:

            liquidity = "LOW"

        return {

            "score": score,

            "liquidity": liquidity,

            "volume_ratio": round(

                volume_ratio,

                2,

            ),

            "spread": round(

                spread,

                2,

            ) if spread is not None else None,

            "reasons": reasons,

        }