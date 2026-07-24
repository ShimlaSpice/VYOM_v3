from app.market.sector_mapper import SectorMapper

mapper = SectorMapper()

symbols = [
    "RELIANCE.NS",
    "ICICIBANK.NS",
    "TCS.NS",
    "INFY.NS",
    "SBIN.NS",
]

print()

print("=" * 60)
print("SECTOR MAPPING")
print("=" * 60)

for symbol in symbols:

    sector = mapper.get_sector(symbol)

    print(f"{symbol:20} {sector}")