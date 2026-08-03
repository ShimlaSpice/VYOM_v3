"""
Risk Intelligence Engine.
"""

from __future__ import annotations


class RiskEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        atr_percent: float,

        volatility: str,

        risk_reward: float,

    ) -> dict:

        score = 0

        reasons = []

        volatility = (

            volatility or "UNKNOWN"

        ).upper()

        if atr_percent <= 0:

            reasons.append(

                "ATR unavailable."

            )

        elif atr_percent < 1:

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

        elif atr_percent < 5:

            score += 2

            reasons.append(

                "High Volatility."

            )

        else:

            score += 1

            reasons.append(

                "Extreme Volatility."

            )

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

        elif volatility == "HIGH":

            reasons.append(

                "High Volatility Environment."

            )

        else:

            reasons.append(

                "Volatility Unknown."

            )

        if risk_reward >= 4:

            score += 3

            reasons.append(

                f"Outstanding Risk Reward ({risk_reward}:1)"

            )

        elif risk_reward >= 3:

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

        else:

            reasons.append(

                f"Poor Risk Reward ({risk_reward}:1)"

            )

        score = min(

            score,

            self.MAX_SCORE,

        )

        if score >= 9:

            risk_level = "LOW"

        elif score >= 6:

            risk_level = "MEDIUM"

        else:

            risk_level = "HIGH"

        return {

            "risk_level": risk_level,

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "reasons": reasons,

        }