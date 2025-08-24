import re

def clean_whitespace(text: str) -> str:
    return re.sub(r"\s{2,}", " ", text.strip())

def safe_get(d: dict, *keys, default=None):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d
