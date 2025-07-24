import os
import praw
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set up Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def test_reddit_connection():
    try:
        subreddit = reddit.subreddit("stocks")
        post = next(subreddit.hot(limit=1))  # Get 1 post from r/stocks
        print("✅ Successfully connected to Reddit.")
        print(f"Title: {post.title}")
        print(f"Author: {post.author}")
        print(f"URL: https://www.reddit.com{post.permalink}")

        post.comments.replace_more(limit=0)
        top_comment = post.comments[0].body if post.comments else "No comments"
        print(f"Top Comment: {top_comment[:120]}...")

    except Exception as e:
        print("❌ Failed to connect or fetch data from Reddit.")
        print("Error:", e)

if __name__ == "__main__":
    test_reddit_connection()
