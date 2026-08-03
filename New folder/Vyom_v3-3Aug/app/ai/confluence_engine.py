"""
Confluence Engine for VYOM.

Calculates how many independent signals agree
with each other.

This is one of Jarvis' core decision engines.
"""

from __future__ import annotations


class ConfluenceEngine:

    def analyze(

        self,

        technical: dict,

        structure: dict,

        trend: dict,

        support: dict,

        candlestick: dict,

        liquidity: dict,

        probability: dict,

    ) -> dict:

        score = 0

        confirmations = []

        # -----------------------------------
        # Technical
        # -----------------------------------

        if technical.get("score", 0) >= 30:

            score += 2

            confirmations.append(

                "Strong Technical Score",

            )

        # -----------------------------------
        # Market Structure
        # -----------------------------------

        if structure.get("trend") == "UPTREND":

            score += 2

            confirmations.append(

                "Bullish Market Structure",

            )

        # -----------------------------------
        # Trend Strength
        # -----------------------------------

        if trend.get("score", 0) >= 8:

            score += 2

            confirmations.append(

                "Strong Trend",

            )

        # -----------------------------------
        # Support / Resistance
        # -----------------------------------

        if support.get("position") in (

            "BREAKOUT",

            "NEAR_SUPPORT",

        ):

            score += 2

            confirmations.append(

                support["position"],

            )

        # -----------------------------------
        # Candlestick
        # -----------------------------------

        if candlestick.get("signal") == "BULLISH":

            score += 2

            confirmations.append(

                candlestick["pattern"],

            )

        # -----------------------------------
        # Liquidity
        # -----------------------------------

        if liquidity.get("score", 0) >= 7:

            score += 1

            confirmations.append(

                "Good Liquidity",

            )

        # -----------------------------------
        # Probability
        # -----------------------------------

        if probability.get("probability", 0) >= 80:

            score += 2

            confirmations.append(

                "High Probability",

            )

        # -----------------------------------

        if score >= 12:

            level = "EXTREME"

        elif score >= 10:

            level = "VERY HIGH"

        elif score >= 8:

            level = "HIGH"

        elif score >= 6:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {

            "score": score,

            "level": level,

            "confirmations": confirmations,

            "count": len(confirmations),

        }