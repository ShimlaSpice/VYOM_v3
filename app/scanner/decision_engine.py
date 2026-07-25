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

        if score >= 90:

            candidate.decision = "STRONG BUY"

            candidate.confidence = 0.95

        elif score >= 75:

            candidate.decision = "BUY"

            candidate.confidence = 0.85

        elif score >= 60:

            candidate.decision = "WATCH"

            candidate.confidence = 0.70

        elif score >= 40:

            candidate.decision = "HOLD"

            candidate.confidence = 0.55

        else:

            candidate.decision = "AVOID"

            candidate.confidence = 0.30

        return candidate