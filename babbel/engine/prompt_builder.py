from __future__ import annotations
from typing import List, Dict, Any

BASE_SYSTEM_MINIMAL = "You are Babbel Assistant. Be concise, helpful, and safe."

BABBEL_PROTOCOL_POLICY = """
# Babbel Protocol (Enforced)
- Tone: clear, non-platitudinous, precise.
- Structure: short paragraphs; bullets only when valuable.
- Honesty: say what you know and what you don't.
- Safety: never give harmful, illegal, or medical advice.
- No purple prose; avoid filler.
- Prefer concrete steps and examples tailored to the user's request.
""".strip()

def build_messages(user_messages: List[Dict[str, Any]], show_metadata: bool) -> List[Dict[str, str]]:
    system = BASE_SYSTEM_MINIMAL + "\n\n" + BABBEL_PROTOCOL_POLICY
    out: List[Dict[str, str]] = [{"role": "system", "content": system}]
    for m in user_messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        out.append({"role": role, "content": content})

    if show_metadata:
        out.append({
            "role": "system",
            "content": "Include a brief, machine-parsable emotion/intent summary if supported by the pipeline."
        })
    else:
        out.append({
            "role": "system",
            "content": "Do not include explicit metadata annotations in the text response."
        })
    return out
