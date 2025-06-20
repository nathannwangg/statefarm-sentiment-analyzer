# PRAW logic
import os
import praw
import os
from dotenv import load_dotenv
from storage import Storage
from analysis import analyze_sentiments

# Initialize SQLite storage
store = Storage()

# Load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = f"MyRedditScraper/0.0.1 by u/{USERNAME}"

# Validate environment variables
if not all([CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD]):
    raise Exception("Missing one or more environment variables. Check your .env file.")

#Configure parameters
SUBREDDIT = "Insurance"
KEYWORDS = ["State Farm", "StateFarm", "SF"]
POST_LIMIT = 500 
FIELDNAMES = ["subreddit", "type", "post_id", "comment_id", "title", "body", "url"]

def get_reddit_client():
    try:
        client = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USERNAME,
            password=PASSWORD,
            user_agent=USER_AGENT
        )
        return client
    except Exception as e:
        print(f"Error: {e}")

def fetch_posts(subreddit_name: str, limit: int = 100):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    results = []
    for sub in subreddit.top(time_filter="month", limit=limit):
        post_text = (sub.title or "") + " " + (sub.selftext or "")
        if any(keyword.lower() in post_text.lower() for keyword in KEYWORDS):
            results.append({
                "id": sub.id,
                "title": sub.title,
                "body": sub.selftext,
                "created_utc": sub.created_utc, #timestamp
                "permalink": f"https://reddit.com{sub.permalink}",
                "comments": [c.body for c in sub.comments if hasattr(c, "body")]
            })
    return results

def run_ingestion(subreddit: str = "Insurance", limit: int = 100):
    raw_data= fetch_posts(subreddit, limit)
    print(f"{len(raw_data)} posts pulled")
    enriched_data= analyze_sentiments(raw_data)
    store.save(enriched_data)
    print(f"Saved {len(enriched_data)} posts to {store.db_path}")


# Run this function to populate database
run_ingestion(subreddit=SUBREDDIT, limit=POST_LIMIT)