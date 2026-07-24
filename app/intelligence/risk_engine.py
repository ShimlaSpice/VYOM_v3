"""
Risk Intelligence Engine.
"""

from __future__ import annotations


class RiskEngine:

    def evaluate(
        self,
        atr_percent: float,
        volatility: str,
        risk_reward: float,
    ) -> dict:

        score = 0

        reasons = []

        risk_level = "HIGH"

        # -------------------------------------
        # ATR %
        # -------------------------------------

        if atr_percent < 1:

            score += 5

            reasons.append(
                "Very Stable Price Movement."
            )

        elif atr_percent < 2:

            score += 4

            reasons.append(
                "Controlled Volatility."
            )

        elif atr_percent < 3:

            score += 3

            reasons.append(
                "Moderate Volatility."
            )

        else:

            score += 1

            reasons.append(
                "High Volatility."
            )

        # -------------------------------------
        # Volatility
        # -------------------------------------

        if volatility == "LOW":

            score += 2

            reasons.append(
                "Low Volatility."
            )

        elif volatility == "MEDIUM":

            score += 1

            reasons.append(
                "Acceptable Volatility."
            )

        # -------------------------------------
        # Risk Reward
        # -------------------------------------

        if risk_reward >= 3:

            score += 3

            reasons.append(
                f"Excellent Risk Reward ({risk_reward}:1)"
            )

        elif risk_reward >= 2:

            score += 2

            reasons.append(
                f"Good Risk Reward ({risk_reward}:1)"
            )

        elif risk_reward >= 1.5:

            score += 1

            reasons.append(
                f"Acceptable Risk Reward ({risk_reward}:1)"
            )

        # -------------------------------------
        # Risk Level
        # -------------------------------------

        if score >= 9:

            risk_level = "LOW"

        elif score >= 6:

            risk_level = "MEDIUM"

        else:

            risk_level = "HIGH"

        score = min(score, 10)

        return {

            "risk_level": risk_level,

            "score": score,

            "max_score": 10,

            "confidence": round(
                (score / 10) * 100
            ),

            "reasons": reasons,

        }