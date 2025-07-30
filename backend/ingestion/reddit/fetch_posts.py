import praw
from dotenv import load_dotenv
import os
import time
from typing import List, Dict

# Load variables from .env file
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def get_reddit_posts(company_name, limit = 20, subreddit_list="stocks+investing+wallstreetbets", sort = "top", time_filter = "week") -> List[Dict]:

    # gather all results
    results = reddit.subreddit(subreddit_list).search(
        query=company_name,
        sort=sort,
        time_filter=time_filter,
        limit=limit
    )

    posts = []

    for post in results:
        body = post.selftext or ""
        full_text = f"{post.title}\n\n{body}".strip()

        posts.append({
            "source": "Reddit",
            "company_name": company_name,
            "id": post.id,
            "title": post.title,
            "body": post.selftext,
            "full_text": full_text,
            "subreddit": str(post.subreddit),
            "author": str(post.author),
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "url": f"https://www.reddit.com{post.permalink}",
            "comments": get_comments(post.id, limit=20)
        })

        # to avoid hitting API call limit
        # time.sleep(1)

    return posts

def get_comments(post_id: str, limit: int = None) -> List[str]:
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    comments = []

    for comment in submission.comments.list():
        if comment.body and comment.body not in ["[deleted]", "[removed]"]:
            if len(comment.body.strip()) >= 10:
                comments.append(comment.body.strip())
            if limit and len(comments) >= limit:
                break

    return comments
