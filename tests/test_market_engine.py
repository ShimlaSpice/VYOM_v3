from app.market import YahooFinanceProvider, MarketEngine

provider = YahooFinanceProvider()
engine = MarketEngine(provider)

candles = engine.load_history("RELIANCE.NS")

print(f"Candles Downloaded: {len(candles)}")

if candles:
    print("\nLatest Candle:")
    print(candles[-1])

quote = engine.load_quote("RELIANCE.NS")

print("\nLive Quote:")
print(quote)