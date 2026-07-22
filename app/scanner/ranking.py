"""
Ranking Engine for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class RankingEngine:
    """
    Ranks scan candidates using weighted scores.
    """

    def rank(
        self,
        candidates: list[ScanCandidate],
    ) -> list[ScanCandidate]:

        return sorted(
            candidates,
            key=lambda candidate: (
                candidate.score,
                candidate.confidence,
            ),
            reverse=True,
        )