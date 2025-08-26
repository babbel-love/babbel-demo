import re

def enforce_babbel_style(text: str) -> str:
    replacements = [
        (r"\bjust\b", ""),
        (r"\bmaybe\b", ""),
        (r"\bperhaps\b", ""),
        (r"\bi think\b", ""),
        (r"\bit seems\b", ""),
        (r"\bi feel like\b", ""),
        (r"\bkinda\b", ""),
        (r"\bsort of\b", ""),
        (r"\bthere (is|are)\b\s*", ""),
        (r"\bit is important to note that\b\s*", ""),
        (r"\bshould\b", "must"),
        (r"\butilize\b", "use"),
        (r"\bcan be\b\s+(\w+)\s+as\b", r"is \1"),
    ]
    out = text
    for pat, repl in replacements:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out).strip()
