from app.recommendation.recommendation_model import Recommendation
from app.top10 import Top10Engine
from app.top10.models import RankedStock


def test_ranked_stock_preserves_ui_fields():
    recommendation = Recommendation(
        symbol="RELIANCE",
        recommendation="BUY",
        category="LARGE_CAP",
        confidence=82,
        probability=80,
        entry=1278,
        stop_loss=1227,
        target1=1403,
        target2=1478,
        risk_level="MEDIUM",
        close=1280,
        sector="ENERGY",
        industry="OIL_GAS",
        ai_summary="Strong breakout",
        reasons=["Momentum", "Support"],
        scores={"technical": 78, "fundamental": 70, "news": 60, "sector": 65, "risk": 55},
    )

    ranked = RankedStock.from_recommendation(recommendation)

    assert ranked.price == 1280
    assert ranked.sector == "ENERGY"
    assert ranked.ai_summary == "Strong breakout"
    assert ranked.reasons == ["Momentum", "Support"]
    assert ranked.scores["technical"] == 78


def test_top10_engine_returns_ranked_results():
    recommendations = [
        Recommendation(
            symbol="RELIANCE",
            recommendation="BUY",
            category="LARGE_CAP",
            confidence=82,
            probability=80,
            entry=1278,
            stop_loss=1227,
            target1=1403,
            target2=1478,
            risk_level="MEDIUM",
            scores={"technical": 78, "fundamental": 70, "news": 60, "sector": 65, "risk": 55},
        ),
        Recommendation(
            symbol="ICICIBANK",
            recommendation="BUY",
            category="LARGE_CAP",
            confidence=91,
            probability=88,
            entry=1450,
            stop_loss=1425,
            target1=1510,
            target2=1560,
            risk_level="LOW",
            scores={"technical": 85, "fundamental": 80, "news": 70, "sector": 75, "risk": 60},
        ),
        Recommendation(
            symbol="TCS",
            recommendation="BUY",
            category="LARGE_CAP",
            confidence=87,
            probability=84,
            entry=3650,
            stop_loss=3580,
            target1=3790,
            target2=3860,
            risk_level="LOW",
            scores={"technical": 82, "fundamental": 77, "news": 65, "sector": 70, "risk": 58},
        ),
    ]

    engine = Top10Engine()
    result = engine.generate(recommendations)

    assert len(result) == 3
    assert result[0].symbol == "ICICIBANK"
    assert result[0].confidence == 91