import sys
import os

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Now use absolute import
from backend.ingestion.gather_data import fetch_data

#from ..backend.ingestion.gather_data import fetch_data

def main():
    data = fetch_data("Tesla", max_reddit_posts = 1)
    post = data[0]

    chunk_a = f"""TITLE: {post['title']}

    BODY:
    {post['body']}

    COMMENTS:
    {chr(10).join(post['comments'])}
    """

    print(chunk_a)

if __name__ == "__main__":
    main()