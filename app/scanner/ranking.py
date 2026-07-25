"""
Ranking Engine for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class RankingEngine:

    def rank(

        self,

        candidates: list[ScanCandidate],

    ) -> list[ScanCandidate]:

        return sorted(

            candidates,

            key=lambda candidate: (

                candidate.score,

                candidate.confidence,

                len(candidate.reasons),

                candidate.symbol,

            ),

            reverse=True,

        )