import certifi, os
os.environ['SSL_CERT_FILE'] = certifi.where()

import sys
import os

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backend.ingestion.X.fetch_x import get_x_posts  # replace with your actual filename/module
import pprint

def test_get_x_posts_basic():
    company = "Tesla"
    posts = get_x_posts(company, time_filter="day", limit=5)

    assert isinstance(posts, list), "Output should be a list"
    assert len(posts) <= 5, "Should return no more than 5 posts"
    
    for post in posts:
        assert isinstance(post, dict), "Each post should be a dictionary"
        assert post.get("source") == "X", "Source should be 'X'"
        assert post.get("company_name") == company, "Company name mismatch"
        assert "body" in post, "Missing 'body' in post"
        assert post["comments"] == "Not Applicable", "Comments should be 'Not Applicable'"

    pprint.pprint(posts)

def test_get_x_posts_invalid_filter():
    posts = get_x_posts("Tesla", time_filter="month", limit=5)
    assert posts == [], "Should return empty list on invalid time_filter"

if __name__ == "__main__":
    test_get_x_posts_basic()
    test_get_x_posts_invalid_filter()
