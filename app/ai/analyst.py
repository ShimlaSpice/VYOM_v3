"""
AI Analyst for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class AIAnalyst:

    def analyze(

        self,

        candidate: ScanCandidate,

    ) -> ScanCandidate:

        reasons = list(

            candidate.reasons

        )

        score = candidate.score

        decision = candidate.decision

        if score >= 90:

            reasons.append(

                "Exceptional technical structure."

            )

        elif score >= 80:

            reasons.append(

                "Strong technical setup."

            )

        elif score >= 65:

            reasons.append(

                "Momentum building."

            )

        elif score >= 50:

            reasons.append(

                "Early signs of strength."

            )

        else:

            reasons.append(

                "Weak technical setup."

            )

        if decision == "STRONG BUY":

            reasons.append(

                "High probability trade."

            )

            reasons.append(

                "Multiple bullish confirmations."

            )

        elif decision == "BUY":

            reasons.append(

                "BUY signal confirmed."

            )

        elif decision == "WATCH":

            reasons.append(

                "Wait for breakout confirmation."

            )

        else:

            reasons.append(

                "Avoid until structure improves."

            )

        candidate.reasons = reasons

        return candidate