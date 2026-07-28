"""
Jarvis Decision Engine for VYOM.

Final AI Brain.
"""

from __future__ import annotations

from app.ai.catalyst_engine import CatalystEngine
from app.ai.conviction_engine import ConvictionEngine
from app.ai.opportunity_engine import OpportunityEngine
from app.ai.probability_engine import ProbabilityEngine
from app.ai.rejection_engine import RejectionEngine


class JarvisEngine:

    def __init__(self):

        self.probability = ProbabilityEngine()

        self.conviction = ConvictionEngine()

        self.catalyst = CatalystEngine()

        self.opportunity = OpportunityEngine()

        self.rejection = RejectionEngine()

    def analyze(

        self,

        technical: dict,

        fundamental: dict,

        news: dict,

        sector: dict,

        risk: dict,

        confidence: dict,

    ) -> dict:

        probability = self.probability.calculate(

            technical=technical["score"],

            fundamental=fundamental["score"],

            news=news["score"],

            sector=sector["score"],

            risk=risk["score"],

            confidence=confidence["confidence"],

        )

        conviction = self.conviction.evaluate(

            probability=probability["probability"],

            confidence=confidence["confidence"],

            technical_score=technical["score"],

            risk_score=risk["score"],

        )

        catalyst = self.catalyst.analyze(

            technical,

            fundamental,

            news,

            sector,

        )

        opportunity = self.opportunity.evaluate(

            probability=probability["probability"],

            conviction=conviction["score"],

            technical_score=technical["score"],

            catalyst_strength=catalyst["strength"],

            risk_score=risk["score"],

        )

        rejection = self.rejection.evaluate(

            technical,

            fundamental,

            news,

            sector,

            risk,

            probability["probability"],

        )

        return {

            "probability": probability,

            "conviction": conviction,

            "catalyst": catalyst,

            "opportunity": opportunity,

            "rejection": rejection,

            "decision": conviction["action"],

        }