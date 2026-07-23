from app.news import NewsEngine

engine = NewsEngine()

news = engine.analyze("RELIANCE.NS")

print(news)