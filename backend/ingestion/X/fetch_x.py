from typing import List, Dict
import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta

def get_x_posts(company: str, time_filter: str = "week", limit: int = 20) -> List[Dict]:

    # Create query
    max_age = 0
    if time_filter == "week":
        max_age = 7
    elif time_filter == "day":
        max_age = 1
    
    if max_age == 0:
        print("X POST AGE ERROR")

    delta = timedelta(days = max_age)
    start_date = datetime.now() - delta
    end_date = datetime.now()
    query = f"{company} since:{start_date} until:{end_date} lang:en"

    # Scraping time
    posts = []
    post_num = 0
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if post_num >= limit:
            break

        posts.append({
            "source": "X",
            "company_name": company,
            "title": "Not Applicable",
            "body": tweet.content,
            "comments": "Not Applicable"
        })
        post_num += 1

    return posts