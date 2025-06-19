# optional FastAPI backend

from fastapi import FastAPI
from ingestion import fetch_posts
from analysis import analyze_sentiments

app = FastAPI()

@app.get("/analyze")
async def analyze(subreddit: str = "technology"):
    posts = fetch_posts(subreddit)
    return analyze_sentiments(posts)

@app.get("/health")
async def health():
    return {"status": "ok"}
