import pytest
from src.ingestion import fetch_posts

def test_fetch_posts_dummy():
    posts = fetch_posts("python", limit=1)
    assert isinstance(posts, list)
    assert "id" in posts[0]
