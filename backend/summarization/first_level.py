import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from typing import List, Dict

def individual_summary(data: List[Dict]):
    return