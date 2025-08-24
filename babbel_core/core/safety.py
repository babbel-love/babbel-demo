from __future__ import annotations
import re
from typing import Tuple, Dict, Any

SELF_HARM_PAT = re.compile(r"\b(kill myself|suicide|end my life)\b", re.IGNORECASE)
PII_PAT = re.compile(r"\b(password|ssn|social security|credit card|cvv)\b", re.IGNORECASE)

def analyze(user_text: str) -> Dict[str, Any]:
    reasons = []
    if SELF_HARM_PAT.search(user_text or ""):
        reasons.append("self_harm")
    if PII_PAT.search(user_text or ""):
        reasons.append("pii")
    return {"blocked": bool(reasons), "reasons": reasons}

def gate(output_text: str) -> Tuple[bool, Dict[str, Any], str]:
    # Minimal output scan; in a real system you'd re-scan and redact if needed.
    blocked = False
    reasons: list[str] = []
    return blocked, {"blocked": blocked, "reasons": reasons}, output_text
