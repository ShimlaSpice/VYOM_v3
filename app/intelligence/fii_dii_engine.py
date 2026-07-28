"""
FII / DII Intelligence Engine.

Analyses institutional buying and selling.
"""

from __future__ import annotations


class FIIDIIEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        fii_net: float,

        dii_net: float,

    ) -> dict:

        score = 5

        reasons = []

        total = fii_net + dii_net

        # ----------------------------------------
        # FII
        # ----------------------------------------

        if fii_net > 1000:

            score += 3

            reasons.append(

                f"Strong FII Buying ({fii_net:.0f} Cr)"

            )

        elif fii_net > 0:

            score += 2

            reasons.append(

                f"Positive FII Buying ({fii_net:.0f} Cr)"

            )

        elif fii_net < -1000:

            score -= 3

            reasons.append(

                f"Heavy FII Selling ({abs(fii_net):.0f} Cr)"

            )

        elif fii_net < 0:

            score -= 2

            reasons.append(

                f"Moderate FII Selling ({abs(fii_net):.0f} Cr)"

            )

        # ----------------------------------------
        # DII
        # ----------------------------------------

        if dii_net > 1000:

            score += 2

            reasons.append(

                f"Strong DII Buying ({dii_net:.0f} Cr)"

            )

        elif dii_net > 0:

            score += 1

            reasons.append(

                f"Positive DII Buying ({dii_net:.0f} Cr)"

            )

        elif dii_net < -1000:

            score -= 2

            reasons.append(

                f"Heavy DII Selling ({abs(dii_net):.0f} Cr)"

            )

        elif dii_net < 0:

            score -= 1

            reasons.append(

                f"Moderate DII Selling ({abs(dii_net):.0f} Cr)"

            )

        # ----------------------------------------
        # Combined Flow
        # ----------------------------------------

        if total > 2000:

            reasons.append(

                "Strong Institutional Inflow"

            )

        elif total < -2000:

            reasons.append(

                "Strong Institutional Outflow"

            )

        score = max(

            0,

            min(

                score,

                self.MAX_SCORE,

            ),

        )

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "fii_net": fii_net,

            "dii_net": dii_net,

            "reasons": reasons,

        }