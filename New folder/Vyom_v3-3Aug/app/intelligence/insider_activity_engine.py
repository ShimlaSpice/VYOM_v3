"""
Insider Activity Intelligence Engine.

Evaluates insider buying and selling.
"""

from __future__ import annotations


class InsiderActivityEngine:

    MAX_SCORE = 10

    def evaluate(

        self,

        promoter_buy: float = 0.0,

        promoter_sell: float = 0.0,

        insider_buy: float = 0.0,

        insider_sell: float = 0.0,

    ) -> dict:

        score = 5

        reasons = []

        # ----------------------------------------
        # Promoter Buying
        # ----------------------------------------

        if promoter_buy > 0:

            score += 2

            reasons.append(

                f"Promoter Buying ({promoter_buy:.2f}%)"

            )

        # ----------------------------------------
        # Promoter Selling
        # ----------------------------------------

        if promoter_sell > 0:

            score -= 2

            reasons.append(

                f"Promoter Selling ({promoter_sell:.2f}%)"

            )

        # ----------------------------------------
        # Insider Buying
        # ----------------------------------------

        if insider_buy > 0:

            score += 2

            reasons.append(

                f"Insider Buying ({insider_buy:.2f}%)"

            )

        # ----------------------------------------
        # Insider Selling
        # ----------------------------------------

        if insider_sell > 0:

            score -= 2

            reasons.append(

                f"Insider Selling ({insider_sell:.2f}%)"

            )

        # ----------------------------------------
        # Combined View
        # ----------------------------------------

        total_buy = promoter_buy + insider_buy

        total_sell = promoter_sell + insider_sell

        if total_buy > total_sell:

            reasons.append(

                "Net Insider Buying"

            )

        elif total_sell > total_buy:

            reasons.append(

                "Net Insider Selling"

            )

        else:

            reasons.append(

                "Neutral Insider Activity"

            )

        score = max(

            0,

            min(

                score,

                self.MAX_SCORE,

            ),

        )

        if score >= 8:

            outlook = "POSITIVE"

        elif score >= 5:

            outlook = "NEUTRAL"

        else:

            outlook = "NEGATIVE"

        return {

            "score": score,

            "max_score": self.MAX_SCORE,

            "confidence": round(

                (score / self.MAX_SCORE) * 100

            ),

            "outlook": outlook,

            "promoter_buy": promoter_buy,

            "promoter_sell": promoter_sell,

            "insider_buy": insider_buy,

            "insider_sell": insider_sell,

            "reasons": reasons,

        }