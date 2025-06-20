from fastapi import FastAPI, HTTPException
from storage import Storage
from text_summarizer import summarize_post, summarize_comments

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
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "permalink": row[3],
            "sentiment": row[4],
        }
        for row in posts
    ]

@app.get("/top-negative")
async def get_top_negative_posts(n: int = 5):
    """Returns top n negative posts"""
    posts = store.get_top_posts(label="Negative", n=n)
    return [
        {
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "permalink": row[3],
            "sentiment": row[4],
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

@app.get("/summarize/{post_id}")
async def get_or_create_summary(post_id: str):
    """
    Returns summaries for a given post.
    If summaries don't exist, they are generated and saved.
    """
    post = store.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # post is a sqlite3.Row, can be accessed by index or key
    text_summary = post["text_summary"]
    comment_summary = post["comment_summary"]

    if text_summary and comment_summary:
        return {"text_summary": text_summary, "comment_summary": comment_summary}

    # Generate summaries if they don't exist
    if not text_summary:
        text_summary = summarize_post(post["title"], post["body"])

    if not comment_summary:
        comments_str = post["comments"]
        comments_list = comments_str.split("\n") if comments_str else []
        # In case there are no comments
        if not comments_list:
            comment_summary = "No comments to summarize."
        else:
            comment_summary = summarize_comments(comments_list)

    # Save to DB
    store.update_summaries(post_id, text_summary, comment_summary)

    return {"text_summary": text_summary, "comment_summary": comment_summary}
