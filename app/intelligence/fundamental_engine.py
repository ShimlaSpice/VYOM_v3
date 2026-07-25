"""
Fundamental Intelligence Engine.
"""

from __future__ import annotations


class FundamentalEngine:

    def evaluate(

        self,

        pe: float | None,

        eps: float | None,

        roe: float | None,

        debt_to_equity: float | None,

        market_cap: int | None,

    ) -> dict:

        score = 0

        reasons = []

        pe = pe or 0
        eps = eps or 0
        roe = roe or 0
        debt_to_equity = debt_to_equity or 0
        market_cap = market_cap or 0

        # ----------------------------------
        # PE
        # ----------------------------------

        if 0 < pe <= 20:

            score += 5

            reasons.append(
                f"Excellent PE ({pe:.2f})"
            )

        elif pe <= 30:

            score += 4

            reasons.append(
                f"Healthy PE ({pe:.2f})"
            )

        elif pe > 30:

            score += 2

            reasons.append(
                f"High PE ({pe:.2f})"
            )

        # ----------------------------------
        # EPS
        # ----------------------------------

        if eps > 50:

            score += 5

            reasons.append(
                f"Strong EPS ({eps:.2f})"
            )

        elif eps > 0:

            score += 3

            reasons.append(
                f"Positive EPS ({eps:.2f})"
            )

        else:

            reasons.append(
                "Negative EPS"
            )

        # ----------------------------------
        # ROE
        # ----------------------------------

        if roe < 1:

            roe = roe * 100

        if roe >= 20:

            score += 5

            reasons.append(
                f"Excellent ROE ({roe:.2f}%)"
            )

        elif roe >= 15:

            score += 4

            reasons.append(
                f"Healthy ROE ({roe:.2f}%)"
            )

        elif roe >= 10:

            score += 2

            reasons.append(
                f"Average ROE ({roe:.2f}%)"
            )

        # ----------------------------------
        # Debt
        # ----------------------------------

        if debt_to_equity == 0:

            reasons.append(
                "Debt data unavailable"
            )

        elif debt_to_equity <= 50:

            score += 3

            reasons.append(
                "Low Debt"
            )

        elif debt_to_equity <= 100:

            score += 2

            reasons.append(
                "Acceptable Debt"
            )

        else:

            reasons.append(
                "High Debt"
            )

        # ----------------------------------
        # Market Cap
        # ----------------------------------

        if market_cap >= 1_000_000_000_000:

            score += 2

            reasons.append(
                "Mega Cap Company"
            )

        elif market_cap >= 100_000_000_000:

            score += 1

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