"""
Candidate Formatter for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class CandidateFormatter:
    """
    Formats scan candidates for display.
    """

    def format(self, candidate: ScanCandidate) -> dict:
        return {
            "symbol": candidate.symbol,
            "decision": candidate.decision,
            "score": round(candidate.score, 2),
            "confidence": round(candidate.confidence * 100, 1),
            "reasons": candidate.reasons,
        }

    def format_all(
        self,
        candidates: list[ScanCandidate],
    ) -> list[dict]:
        return [
            self.format(candidate)
            for candidate in candidates
        ]