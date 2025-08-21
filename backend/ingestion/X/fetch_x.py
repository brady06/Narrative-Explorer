from typing import List, Dict
from datetime import datetime, timedelta
from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Company should be stock ticker here
def get_x_posts(company: str, time_filter: str = "week", limit: int = 40) -> List[Dict]:

    # Create query
    max_age = 0
    if time_filter == "week":
        max_age = 7
    elif time_filter == "day":
        max_age = 1
    
    if max_age == 0:
        print("X POST AGE ERROR")

    # delta = timedelta(days = max_age)
    # start_date = datetime.now() - delta
    # end_date = datetime.now()

    end = datetime.now()
    start = end - timedelta(days=max_age)
    start_date = start.strftime("%Y-%m-%d_%H:%M:%S_UTC")
    end_date = end.strftime("%Y-%m-%d_%H:%M:%S_UTC")

    run_input = {
        "maxItems": limit,
        "searchTerms": [
            f"${company} sentiment",
        ],
        "since": start_date,
        "until": end_date,
        "lang": "en",
        "queryType": "Top"
    }

    # Run the actor
    run = client.actor("CJdippxWmn9uRfooo").call(run_input=run_input)

    # Scraping time
    posts = []
    for tweet in client.dataset(run["defaultDatasetId"]).iterate_items():
        posts.append({
            "source": "X",
            "company_name": company,
            "title": "Not Applicable",
            "body": tweet["text"],
            "comments": "Not Applicable",
            "url": tweet.get("url") or tweet.get("twitterUrl") or f"https://twitter.com/i/web/status/{tweet['id']}"
        })

    return posts

# if __name__ == "__main__":
#     company = "TSLA"
#     posts = get_x_posts(company, time_filter="week", limit=20)  # pull 5 just in case

#     for i, post in enumerate(posts[:20]):  # print first 2
#         print(f"\nPost {i+1}:")
#         print(f"Text: {post['body']}")
#         print(f"URL: {post['url']}")