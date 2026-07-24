from app.intelligence import ConfidenceEngine

engine = ConfidenceEngine()

result = engine.calculate(

    technical=30,

    fundamental=18,

    news=8,

    sector=9,

    relative_strength=10,

    market=8,

    risk=4,

)

print()

print("=" * 60)

print("CONFIDENCE ENGINE")

print("=" * 60)

print()

print(

    f"Confidence : {result['confidence']}%"

)

print(

    f"Grade      : {result['grade']}"

)

print()

print("Breakdown")

print("-" * 60)

for key, value in result["breakdown"].items():

    print(f"{key:20} {value}")
    