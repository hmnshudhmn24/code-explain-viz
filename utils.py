# utils.py
import re

def extract_first_function_name(code: str):
    m = re.search(r"def\s+([A-Za-z0-9_]+)\s*\(", code)
    return m.group(1) if m else None
