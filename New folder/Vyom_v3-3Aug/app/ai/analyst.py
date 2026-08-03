"""
AI Analyst for VYOM.
"""

from __future__ import annotations

from app.scanner.models import ScanCandidate


class AIAnalyst:

    _CACHE: dict[tuple, list[str]] = {}

    def analyze(

        self,

        candidate: ScanCandidate,

    ) -> ScanCandidate:

        key = (

            candidate.score,

            candidate.decision,

            candidate.breakout,

            round(

                candidate.rsi,

                1,

            ),

            round(

                candidate.relative_strength,

                2,

            ),

        )

        cached = self._CACHE.get(

            key,

        )

        if cached is not None:

            candidate.reasons = list(

                cached,

            )

            return candidate

        reasons = list(

            candidate.reasons,

        )

        score = candidate.score

        if score >= 7:

            reasons.append(

                "Strong technical structure."

            )

        elif score >= 6:

            reasons.append(

                "Momentum improving."

            )

        elif score >= 5:

            reasons.append(

                "Watch for confirmation."

            )

        else:

            reasons.append(

                "Weak technical structure."

            )

        if candidate.breakout:

            reasons.append(

                "Breakout confirmed."

            )

        if candidate.relative_strength > 1:

            reasons.append(

                "Outperforming market."

            )

        decision = candidate.decision

        if decision == "STRONG BUY":

            reasons.extend(

                [

                    "Multiple bullish confirmations.",

                    "High conviction setup.",

                ]

            )

        elif decision == "BUY":

            reasons.append(

                "Favorable risk-reward."

            )

        elif decision == "WATCH":

            reasons.append(

                "Wait for trigger."

            )

        else:

            reasons.append(

                "Avoid until conditions improve."

            )

        self._CACHE[key] = list(

            reasons,

        )

        candidate.reasons = reasons

        return candidate

    @classmethod
    def clear_cache(

        cls,

    ):

        cls._CACHE.clear()