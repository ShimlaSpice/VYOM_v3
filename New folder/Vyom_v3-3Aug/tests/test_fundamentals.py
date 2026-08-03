from app.fundamentals import FundamentalEngine

engine = FundamentalEngine()

fundamental = engine.analyze(
    "RELIANCE.NS"
)

print()

print("=" * 60)

for key, value in fundamental.items():
    print(f"{key:20}: {value}")