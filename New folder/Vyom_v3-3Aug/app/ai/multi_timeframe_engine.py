"""
Multi Timeframe Analysis Engine.
"""

from __future__ import annotations


class MultiTimeframeEngine:

    def evaluate(

        self,

        weekly: bool,

        daily: bool,

        four_hour: bool,

        one_hour: bool,

    ) -> dict:

        score = 0

        reasons = []

        if weekly:
            score += 3
            reasons.append("Weekly Trend Bullish")

        if daily:
            score += 3
            reasons.append("Daily Trend Bullish")

        if four_hour:
            score += 2
            reasons.append("4H Trend Bullish")

        if one_hour:
            score += 2
            reasons.append("1H Trend Bullish")

        if score >= 9:
            alignment = "VERY STRONG"

        elif score >= 7:
            alignment = "STRONG"

        elif score >= 5:
            alignment = "MODERATE"

        else:
            alignment = "WEAK"

        return {

            "score": score,

            "alignment": alignment,

            "reasons": reasons,

        }