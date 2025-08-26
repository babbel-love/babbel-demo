from __future__ import annotations
import re

def _soften_imperatives(text: str) -> str:
    # Replace hard imperatives with suggestions
    t = re.sub(r"(?i)\b(do|use|pick|choose|stop|start)\b", lambda m: {"do":"try","use":"consider","pick":"choose","choose":"consider","stop":"try pausing","start":"try"}[m.group(0).lower()], text)
    t = re.sub(r"(?i)\bmust\b", "might", t)
    t = re.sub(r"(?i)\byou need to\b", "you could", t)
    return t

def apply_and_explain(text: str, src: str="en", dst: str="en") -> tuple[str,str]:
    softened = _soften_imperatives(text)
    if softened != text:
        expl = "Softened direct imperatives into suggestions to match a more indirect/courteous tone."
    else:
        expl = "No cultural shift applied; tone already courteous."
    return softened, expl
