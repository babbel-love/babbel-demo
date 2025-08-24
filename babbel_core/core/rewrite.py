from __future__ import annotations
import re

def rewrite_response(text: str) -> str:
    t = re.sub(r"\b(I think|perhaps|maybe|it seems)\b", "", text, flags=re.IGNORECASE)
    t = re.sub(r"\b(as an AI|I'm here to help|I hope this helps|I apologize)\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()
