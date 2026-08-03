from app.news import NewsEngine

engine = NewsEngine()

news = engine.analyze(
    "RELIANCE.NS",
)

print()

print("=" * 60)
print(news["symbol"])
print("=" * 60)

print(f"Sentiment : {news['sentiment']}")
print(f"Confidence: {news['confidence']}")

print()

print("Latest Headlines")

print("-" * 60)

for item in news["headlines"]:

    print(f"• {item['title']}")