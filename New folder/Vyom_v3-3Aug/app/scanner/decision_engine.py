"""
Decision Engine.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class DecisionEngine:

    def evaluate(

        self,

        candidate: ScanCandidate,

    ) -> ScanCandidate:

        score = candidate.score

        if score >= 7:

            candidate.decision = "STRONG BUY"

            candidate.confidence = 95

        elif score >= 6:

            candidate.decision = "BUY"

            candidate.confidence = 88

        elif score >= 5:

            candidate.decision = "WATCH"

            candidate.confidence = 75

        elif score >= 3:

            candidate.decision = "HOLD"

            candidate.confidence = 55

        else:

            candidate.decision = "AVOID"

            candidate.confidence = 30

        return candidate