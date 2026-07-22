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
        """
        Explain why the stock received its score.
        """

        candidate.reasons.clear()

        if candidate.score >= 80:
            candidate.reasons.append(
                "Strong technical setup detected."
            )

        elif candidate.score >= 60:
            candidate.reasons.append(
                "Momentum is improving."
            )

        else:
            candidate.reasons.append(
                "No high-probability setup detected."
            )

        if candidate.decision == "BUY":
            candidate.reasons.append(
                "Price is trading above key moving averages."
            )

        elif candidate.decision == "WATCH":
            candidate.reasons.append(
                "Monitor for confirmation before entry."
            )

        else:
            candidate.reasons.append(
                "Capital preservation preferred."
            )

        return candidate