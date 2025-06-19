# PRAW logic
import os
import praw
import os
from dotenv import load_dotenv
from src.storage import Storage
#from analysis import analyze_sentiments

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
SUBREDDITS = ["Insurance"]
KEYWORDS = ["State Farm"]
POST_LIMIT = 1
OUTPUT_FILE = "results.txt"
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
    for sub in subreddit.new(limit=limit):
        sub.comments.replace_more(limit=0)
        results.append({
            "id": sub.id,
            "title": sub.title,
            "body": sub.selftext,
            "created_utc": sub.created_utc, #timestamp
            "comments": [c.body for c in sub.comments if hasattr(c, "body")]
        })
        results.append(sub)
    return results
