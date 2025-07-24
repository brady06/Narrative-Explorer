from typing import List, Dict
from reddit.fetch_posts import get_reddit_posts

def fetch_data(query: str, max_time: str = "week", max_reddit_posts: int = 50, max_twitter_posts: int = 50, max_news_posts: int = 50) -> List[Dict]:

    # Call all individual methods to gather List of Dict

    all_posts = get_reddit_posts(query, max_reddit_posts, time_filter = max_time)
    # all_posts.extend(other data source here)
    # etc ...

    return all_posts