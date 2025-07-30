import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backend.ingestion.gather_data import fetch_data
from backend.summarization.first_level import first_level_summary
from backend.summarization.second_level import second_level_summary

def get_narratives(company: str, max_time: str = "week", max_reddit_posts: int = 20, max_twitter_posts: int = 20, max_news_posts: int = 20):
    # Gather data
    data = fetch_data(company, max_time = max_time, max_reddit_posts = max_reddit_posts, max_twitter_posts = max_twitter_posts, max_news_posts = max_news_posts)

    # Summarize
    first_level = first_level_summary(data)
    second_level = second_level_summary(first_level, company)

    # Split individual narratives into the summary and then quotes / evidence
    narratives = []
    for narrative in second_level:
        narratives.append(narrative.strip().split("\n"))

    # index 0 will always be the narrative, while the rest of the indecies will be quotes or the like
    return narratives