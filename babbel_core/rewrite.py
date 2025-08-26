import re

_HEDGES = [r"\bjust\b", r"\bmaybe\b", r"\bperhaps\b", r"\bi think\b", r"\bit seems\b", r"\bi feel like\b", r"\bkinda\b", r"\bsort of\b"]

_WEAK_PHRASES = [
    (r"\bit is (very )?important to note that\b\s*", ""),
    (r"\bthere (is|are)\b\s*", ""),
    (r"\bshould\b", "must"),
    (r"\butilize\b", "use"),
    (r"\bcan be\b\s+(\w+)\s+as\b", r"is \1"),
]

def rewrite_tone(text: str) -> str:
    out = text
    for pat in _HEDGES:
        out = re.sub(pat, "", out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out).strip()

def enforce_babbel_style(text: str) -> str:
    out = text
    for pat, repl in _WEAK_PHRASES:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out).strip()

def rewrite_response(text: str) -> str:
    return enforce_babbel_style(rewrite_tone(text)).strip()
