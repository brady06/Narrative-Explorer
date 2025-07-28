import sys
import os
import openai
from typing import List
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

with open(os.path.join(parent_dir, "backend", "summarization", "prompts", "second_level_prompt.txt"), "r", encoding="utf-8") as f:
    prompt_template = f.read()

def second_level_summary(data: List[str], company: str) -> List[str]:
    chunk = "\n\n".join(data)
    prompt = f"The company you will be reporting on is {company}\n\n{chunk}"
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_template.strip()},
            {"role": "user", "content": chunk}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    seperated_narratives = response.choices[0].message.content.strip().split("----------")
    if not seperated_narratives[-1] or seperated_narratives[-1] == '':
        seperated_narratives.pop

    return seperated_narratives