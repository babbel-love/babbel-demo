from __future__ import annotations
from typing import Tuple

SOFTEN_WORDS = {
    "should": "could",
    "must": "might",
    "always": "often",
    "never": "rarely",
}

def apply_and_explain(text: str) -> Tuple[str, str]:
    if not isinstance(text, str) or not text.strip():
        return text, "left unchanged"
    lowered = text.lower()
    hits = [w for w in SOFTEN_WORDS if f" {w} " in f" {lowered} "]
    if not hits:
        return text, "left unchanged"
    out = text
    for src, repl in SOFTEN_WORDS.items():
        out = out.replace(f" {src} ", f" {repl} ")
        out = out.replace(f" {src}.", f" {repl}.")
        out = out.replace(f" {src},", f" {repl},")
    return out, "softened directive tone"
