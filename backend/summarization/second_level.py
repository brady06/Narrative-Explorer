import sys
import os
import openai
from typing import List
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

with open(os.path.join(parent_dir, "prompts", "second_level_prompt.txt"), "r") as f:
    prompt_template = f.read()

def second_level_summary(data: List[str]) -> List[str]:
    chunk = "\n\n".join(data)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_template.strip()},
            {"role": "user", "content": chunk}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    seperated_narratives = response.split("----------")
    
    return seperated_narratives