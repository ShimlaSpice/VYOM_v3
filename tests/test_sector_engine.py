from app.market import YahooFinanceProvider
from app.market.sector_engine import SectorEngine

provider = YahooFinanceProvider()

engine = SectorEngine(provider)

print("\n====== SECTOR STRENGTH ======\n")

for sector in engine.analyze():
    print(
        f"{sector['sector']:10} {sector['change']:>7.2f}%"
    )