from typing import List, Dict
from datetime import datetime, timedelta
from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Company should be stock ticker here
def get_google_news(company: str, time_filter: str = "week", limit: int = 10) -> List[Dict]:

    # Create query
    max_age = 0
    if time_filter == "week":
        max_age = 7
    elif time_filter == "day":
        max_age = 1
    
    if max_age == 0:
        print("GOOGLE POST AGE ERROR")

    end = datetime.now()
    start = end - timedelta(days=max_age)
    start_date = start.strftime("%Y-%m-%d")

    # example format
    # google.com/search?q=tesla+sentiment+after%3A2025-08-21&tbm=nws

    query = f"{company} sentiment news after:{start_date}"
    print("Google Query: " + query)

    run_input = {
        "queries": query,
        "resultsPerPage": limit,
        "maxPagesPerQuery": 1,
        "aiMode": "aiModeOff",
        "focusOnPaidAds": False,
        "searchLanguage": "",
        "languageCode": "",
        "forceExactMatch": False,
        "wordsInTitle": [],
        "wordsInText": [],
        "wordsInUrl": [],
        "mobileResults": False,
        "includeUnfilteredResults": False,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": True,
        "includeIcons": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("nFJndFXA5zjCTuudP").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        print("----------------------")

    posts = []

    for runs in client.dataset(run["defaultDatasetId"]).iterate_items():
        print("Adding something")
        for post in runs.get("organicResults"):
            posts.append({
                "source": "Google",
                "company_name": company,
                "title": post.get("title"),
                "body": parse_website_text(post["url"]),
                "comments": "Not Applicable",
                "url": post["url"]
            })

    return posts

def parse_website_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Tags we want to keep, in order
    tags_to_extract = ["h1", "h2", "h3", "p"]

    content_parts = []
    for tag in soup.find_all(tags_to_extract):
        text = tag.get_text(strip=True)
        if not text:
            continue

        # Add markdown-style formatting so it's clear what's a header
        if tag.name == "h1":
            content_parts.append(f"# {text}")
        elif tag.name == "h2":
            content_parts.append(f"## {text}")
        elif tag.name == "h3":
            content_parts.append(f"### {text}")
        else:  # paragraph
            content_parts.append(text)

    return "\n\n".join(content_parts)


def main():
    company = "AMZN"  # change ticker if needed
    posts = get_google_news(company, time_filter="week", limit=1)

    for i, post in enumerate(posts, start=1):
        print(f"Result {i}:")
        print(f"Title: {post.get('title')}")
        print(f"URL: {post.get('url')}")
        print(f"Body: {post.get('body')}")
        print("-" * 50)


if __name__ == "__main__":
    main()