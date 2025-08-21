from __future__ import annotations
import re
from typing import Tuple

# Very light-touch, opt-in tone adjustments with a short explanation string.
# Goal: reduce friction across communication norms (high-context vs low-context),
# not to stereotype or rewrite content.

def _soften_imperatives(text: str) -> str:
    out_lines = []
    for ln in text.splitlines():
        ln_strip = ln.lstrip()
        # soften "Pick/Choose/Try/Do/Write/Set/List/Give" -> "Consider ..."  (grammar fix)
        out = re.sub(r"^(•\s*)?(Pick|Choose|Try|Do|Write|Set|List|Give)\b", r"\1Consider", ln_strip, flags=re.IGNORECASE)
        # soften "Schedule" -> "You could schedule"
        out = re.sub(r"^(•\s*)?(Schedule)\b", r"\1You could schedule", out, flags=re.IGNORECASE)
        # soften "Ask" -> "You might ask"
        out = re.sub(r"^(•\s*)?(Ask)\b", r"\1You might ask", out, flags=re.IGNORECASE)
        # keep original indentation/bullets
        prefix = ln[: len(ln) - len(ln_strip)]
        out_lines.append(prefix + out)
    return "\n".join(out_lines)

def _sharpen_hedges(text: str) -> str:
    # remove weak hedges "maybe/perhaps/you could/consider" at sentence start
    out = re.sub(r"(?m)^\s*(maybe|perhaps|you could|consider)\s+", "", text, flags=re.IGNORECASE)
    out = re.sub(r"\bkind of\b", "", out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out)

def apply_and_explain(text: str, target: str) -> Tuple[str, str]:
    t = (target or "").strip().lower()
    if not t:
        return text, ""
    if t in {"ja","jp","ja-jp","japanese"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone softened for a higher‑context audience (more permission‑based phrasing, fewer direct imperatives)."
        return adjusted, expl
    if t in {"de","de-de","german"}:
        adjusted = _sharpen_hedges(text)
        expl = "Tone sharpened for a lower‑context audience (clearer directives, fewer hedges)."
        return adjusted, expl
    if t in {"ar","ar-eg","ar-sa","arabic"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone slightly softened and made more invitational."
        return adjusted, expl
    if t in {"zh","zh-cn","zh-tw","cn","chinese"}:
        adjusted = _sharpen_hedges(text)
        expl = "Tone made more direct and pragmatic, minimizing softeners."
        return adjusted, expl
    if t in {"es","es-es","es-mx","spanish"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone softened slightly to reduce direct imperatives."
        return adjusted, expl
    if t in {"fr","fr-fr","french"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone tempered slightly to sound less prescriptive."
        return adjusted, expl
    if t in {"en-us","us","english","en"}:
        return text, "Default directness retained."
    # Unknown target: leave unchanged
    return text, f"No culture profile for “{target}”; left unchanged."
