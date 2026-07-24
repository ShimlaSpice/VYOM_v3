from app.top10 import (
    Top10Engine,
    RankedStock,
)

stocks = [

    RankedStock(
        symbol="RELIANCE",
        recommendation="BUY",
        confidence=82,
        score=82,
        entry=1278,
        stop_loss=1227,
        target1=1403,
        target2=1478,
        risk_level="MEDIUM",
    ),

    RankedStock(
        symbol="ICICIBANK",
        recommendation="BUY",
        confidence=91,
        score=91,
        entry=1450,
        stop_loss=1425,
        target1=1510,
        target2=1560,
        risk_level="LOW",
    ),

    RankedStock(
        symbol="TCS",
        recommendation="BUY",
        confidence=87,
        score=87,
        entry=3650,
        stop_loss=3580,
        target1=3790,
        target2=3860,
        risk_level="LOW",
    ),

]

engine = Top10Engine()

result = engine.generate(stocks)

print()

print("=" * 70)
print("VYOM TOP OPPORTUNITIES")
print("=" * 70)

for i, stock in enumerate(result, start=1):

    print(

        f"{i:02d}. "

        f"{stock.symbol:15}"

        f"{stock.recommendation:8}"

        f"{stock.confidence}%"

    )