# test_narratives.py

import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backend.run_backend import get_narratives 

if __name__ == "__main__":
    company = "Amazon"
    results = get_narratives(company)

    for idx, narrative in enumerate(results, start=1):
        print(narrative[0])
        for quote in narrative[1:]:
            print(quote)
