"""
Fundamental Intelligence Engine.
"""

from __future__ import annotations


class FundamentalEngine:

    def evaluate(
        self,
        pe: float,
        eps: float,
        roe: float | None,
        debt_to_equity: float | None,
        market_cap: int,
    ) -> dict:

        reasons = []

        score = 0

        # -------------------------------------
        # PE Ratio
        # -------------------------------------

        if 0 < pe <= 25:

            score += 5

            reasons.append(
                f"Healthy PE ({pe:.2f})"
            )

        # -------------------------------------
        # EPS
        # -------------------------------------

        if eps > 0:

            score += 5

            reasons.append(
                f"Positive EPS ({eps:.2f})"
            )

        # -------------------------------------
        # ROE
        # -------------------------------------

        if roe is not None:

            roe_percent = roe * 100 if roe < 1 else roe

            if roe_percent >= 15:

                score += 5

                reasons.append(
                    f"Strong ROE ({roe_percent:.2f}%)"
                )

        # -------------------------------------
        # Debt
        # -------------------------------------

        if debt_to_equity is not None:

            if debt_to_equity <= 100:

                score += 3

                reasons.append(
                    "Healthy Debt Level"
                )

        # -------------------------------------
        # Market Cap
        # -------------------------------------

        if market_cap >= 100_000_000_000:

            score += 2

            reasons.append(
                "Large Cap Company"
            )

        confidence = round(
            (score / 20) * 100
        )

        return {

            "score": score,

            "max_score": 20,

            "confidence": confidence,

            "reasons": reasons,

        }