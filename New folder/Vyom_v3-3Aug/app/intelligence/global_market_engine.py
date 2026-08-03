"""
Global Market Intelligence Engine.

Evaluates the impact of major global markets on
Indian equities.
"""

from __future__ import annotations


class GlobalMarketEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        dow_change: float,

        nasdaq_change: float,

        sp500_change: float,

        gift_nifty_change: float,

        crude_change: float,

        usd_inr_change: float,

        vix_change: float,

    ) -> dict:

        score = 5

        reasons = []

        # ----------------------------------------
        # US Markets
        # ----------------------------------------

        us_average = (

            dow_change

            + nasdaq_change

            + sp500_change

        ) / 3

        if us_average >= 1:

            score += 2

            reasons.append(

                "US Markets Bullish"

            )

        elif us_average <= -1:

            score -= 2

            reasons.append(

                "US Markets Bearish"

            )

        else:

            reasons.append(

                "US Markets Mixed"

            )

        # ----------------------------------------
        # GIFT NIFTY
        # ----------------------------------------

        if gift_nifty_change >= 0.50:

            score += 2

            reasons.append(

                "Positive GIFT NIFTY"

            )

        elif gift_nifty_change <= -0.50:

            score -= 2

            reasons.append(

                "Negative GIFT NIFTY"

            )

        # ----------------------------------------
        # Crude Oil
        # ----------------------------------------

        if crude_change <= -2:

            score += 1

            reasons.append(

                "Falling Crude Supports India"

            )

        elif crude_change >= 2:

            score -= 1

            reasons.append(

                "Rising Crude Creates Pressure"

            )

        # ----------------------------------------
        # USD / INR
        # ----------------------------------------

        if usd_inr_change <= -0.30:

            score += 1

            reasons.append(

                "Rupee Strengthening"

            )

        elif usd_inr_change >= 0.30:

            score -= 1

            reasons.append(

                "Rupee Weakening"

            )

        # ----------------------------------------
        # India VIX
        # ----------------------------------------

        if vix_change <= -5:

            score += 1

            reasons.append(

                "Volatility Cooling"

            )

        elif vix_change >= 5:

            score -= 2

            reasons.append(

                "Market Fear Increasing"

            )

        score = max(

            0,

            min(

                score,

                self.MAX_SCORE,

            ),

        )

        if score >= 8:

            outlook = "BULLISH"

        elif score >= 5:

            outlook = "NEUTRAL"

        else:

            outlook = "BEARISH"

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "outlook": outlook,

            "reasons": reasons,

        }