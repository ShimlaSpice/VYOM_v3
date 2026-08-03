"""
Fundamental Intelligence Engine.
"""

from __future__ import annotations


class FundamentalEngine:

    MAX_SCORE = 20

    def evaluate(

        self,

        pe: float | None,

        eps: float | None,

        roe: float | None,

        debt_to_equity: float | None,

        market_cap: int,

    ) -> dict:

        score = 0

        reasons = []

        if pe is None or pe <= 0:

            reasons.append(

                "PE unavailable"

            )

        elif pe <= 20:

            score += 5

            reasons.append(

                f"Excellent PE ({pe:.2f})"

            )

        elif pe <= 30:

            score += 4

            reasons.append(

                f"Healthy PE ({pe:.2f})"

            )

        else:

            reasons.append(

                f"High PE ({pe:.2f})"

            )

        if eps is None:

            reasons.append(

                "EPS unavailable"

            )

        elif eps > 0:

            score += 5

            reasons.append(

                f"Strong EPS ({eps:.2f})"

            )

        else:

            reasons.append(

                "Negative EPS"

            )

        if roe is None:

            reasons.append(

                "ROE unavailable"

            )

        else:

            roe_percent = roe * 100 if roe <= 1 else roe

            if roe_percent >= 20:

                score += 5

                reasons.append(

                    f"Excellent ROE ({roe_percent:.2f}%)"

                )

            elif roe_percent >= 15:

                score += 4

                reasons.append(

                    f"Healthy ROE ({roe_percent:.2f}%)"

                )

            elif roe_percent >= 10:

                score += 3

                reasons.append(

                    f"Average ROE ({roe_percent:.2f}%)"

                )

            else:

                reasons.append(

                    f"Weak ROE ({roe_percent:.2f}%)"

                )

        if debt_to_equity is None:

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

                "Healthy Debt"

            )

        else:

            reasons.append(

                "High Debt"

            )

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

            (score / self.MAX_SCORE) * 100

        )

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": confidence,

            "reasons": reasons,

        }