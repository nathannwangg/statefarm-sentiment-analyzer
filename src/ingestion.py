# PRAW logic

import os
import praw

def get_reddit_client():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

def fetch_posts(subreddit_name: str, limit: int = 100):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    results = []
    for sub in subreddit.new(limit=limit):
        results.append({
            "id": sub.id,
            "title": sub.title,
            "body": sub.selftext,
            "created_utc": sub.created_utc,
            "comments": [c.body for c in sub.comments if hasattr(c, "body")]
        })
    return results
