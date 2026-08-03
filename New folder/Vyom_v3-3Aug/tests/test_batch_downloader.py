from app.market import BatchDownloader, YahooFinanceProvider

provider = YahooFinanceProvider()

downloader = BatchDownloader(provider)

symbols = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "SBIN.NS",
    "HDFCBANK.NS",
]

results = downloader.download_history(symbols)

print()

for symbol, candles in results.items():
    print(
        f"{symbol:<15}"
        f"{len(candles):>5} candles"
    )