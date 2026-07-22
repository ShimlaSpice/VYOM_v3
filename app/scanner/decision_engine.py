"""
Decision Engine for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class DecisionEngine:
    """
    Converts a numerical score into a trading decision.
    """

    BUY_SCORE = 80
    WATCH_SCORE = 60

    def evaluate(self, candidate: ScanCandidate) -> ScanCandidate:
        """
        Assign BUY / WATCH / HOLD based on score.
        """

        if candidate.score >= self.BUY_SCORE:
            candidate.decision = "BUY"
            candidate.confidence = 0.90

        elif candidate.score >= self.WATCH_SCORE:
            candidate.decision = "WATCH"
            candidate.confidence = 0.70

        else:
            candidate.decision = "HOLD"
            candidate.confidence = 0.50

        return candidate