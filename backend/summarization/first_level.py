import sys
import os
import openai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

with open(os.path.join(parent_dir, "backend", "summarization", "prompts", "reddit_prompt.txt"), "r") as f:
    prompt_template = f.read()


def first_level_summary(data: List[Dict]):
    summary_list = []

    for post in data:
        comments = "\n".join(post.get("comments", []))
        chunk = f"POST TITLE: {post['title']}\n\nBODY:\n{post['body']}\n\nCOMMENTS:\n{comments}"

        company_chunk = f"The company you are analysing today is {post['company_name']}"

        full_prompt = f"{company_chunk}\n\nReddit discussion chunk:\n\n{chunk}"

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_template.strip()},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )

        summary = response.choices[0].message.content.strip()
        summary_list.append(summary)

    return summary_list