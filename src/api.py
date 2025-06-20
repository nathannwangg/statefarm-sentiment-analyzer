from fastapi import FastAPI
from storage import Storage

app = FastAPI()
store = Storage()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/top-positive")
async def get_top_positive_posts(n: int = 5):
    """Returns top n positive posts"""
    posts = store.get_top_posts(label="Positive", n=n)
    return [
        {
            "title": row[0],
            "body": row[1],
            "permalink": row[2],
            "sentiment": row[3],
        }
        for row in posts
    ]

@app.get("/top-negative")
async def get_top_negative_posts(n: int = 5):
    """Returns top n negative posts"""
    posts = store.get_top_posts(label="Negative", n=n)
    return [
        {
            "title": row[0],
            "body": row[1],
            "permalink": row[2],
            "sentiment": row[3],
        }
        for row in posts
    ]

@app.get("/sentiment-summary")
async def sentiment_summary():
    """Returns a summary of all sentiments"""
    return store.get_sentiment_summary()

@app.get("/daily-summary")
async def daily_summary(days: int = 7):
    """Returns a daily summary of sentiments for the last n days"""
    daily_counts = store.get_daily_counts(days=days)
    return [
        {"day": row[0], "positive": row[1], "neutral": row[2], "negative": row[3]}
        for row in daily_counts
    ]
