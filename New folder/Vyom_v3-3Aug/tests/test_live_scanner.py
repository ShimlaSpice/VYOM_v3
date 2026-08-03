from app.market import YahooFinanceProvider
from app.scanner.scanner import ScannerEngine

provider = YahooFinanceProvider()

scanner = ScannerEngine(provider)

result = scanner.scan()

print("\n" + "=" * 70)
print("VYOM LIVE SCANNER")
print("=" * 70)

for candidate in result.candidates:

    print(
        f"{candidate.symbol:<18}"
        f"{candidate.score:>5}"
        f"   "
        f"{candidate.decision:<8}"
        f"{candidate.confidence*100:>6.1f}%"
    )

    for reason in candidate.reasons:
        print(f"      • {reason}")

    print()
    