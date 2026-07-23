"""
AI Analyst for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class AIAnalyst:
    """
    Generates human-readable trading insights.
    """

    def analyze(self, candidate: ScanCandidate) -> ScanCandidate:

        # Preserve ScoreCard reasons
        reasons = list(candidate.reasons)

        if candidate.score >= 80:
            reasons.append("Strong technical setup detected.")

        elif candidate.score >= 60:
            reasons.append("Momentum is improving.")

        else:
            reasons.append("Score below BUY threshold.")

        if candidate.decision == "BUY":
            reasons.append("BUY signal confirmed.")

        elif candidate.decision == "WATCH":
            reasons.append("Watch for confirmation.")

        else:
            reasons.append("Capital preservation preferred.")

        candidate.reasons = reasons

        return candidate