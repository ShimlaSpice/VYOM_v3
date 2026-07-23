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

        if score >= 80:
            candidate.decision = "BUY"
            candidate.confidence = 0.90

        elif score >= 60:
            candidate.decision = "WATCH"
            candidate.confidence = 0.75

        else:
            candidate.decision = "HOLD"
            candidate.confidence = 0.50



        return candidate