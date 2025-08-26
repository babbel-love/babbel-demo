#!/bin/bash
cd "$(git rev-parse --show-toplevel || pwd)"

cat <<'PY' > babbel_core/pipeline.py
import re
from .rewrite import rewrite_tone, enforce_babbel_style
from .emotion_classifier import classify_emotion
from .intent_classifier import classify_intent
from .node_rules import apply_node_rules

FACT_FLAG_WORDS = ("latest", "today", "as of", "currently", "expected", "estimated", "about", "roughly")

def run_pipeline(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return "No input."

    emotion = classify_emotion(prompt)
    intent = classify_intent(prompt)
    node_nudge = apply_node_rules(prompt, emotion, intent)
    toned = rewrite_tone(node_nudge)
    final_text = enforce_babbel_style(toned).strip()

    flags = [w for w in FACT_FLAG_WORDS if w in prompt.lower()]
    if re.search(r"\d", prompt): flags.append("number")
    flags = sorted(set(flags))
    fact = f"[Fact-check] Output requires validation: {', '.join(flags)}." if flags else "[Fact-check] No factual red flags detected."

    return (
        f"Final Answer: {final_text}\n\n"
        f"Quick check:\n- Style: Babbel voice enforced\n- Fact flags: {', '.join(flags) if flags else 'none'}\n- Tone: direct, concise\n\n"
        f"— Traces —\nEmotion: {emotion}\nIntent: {intent}\nNode: {node_nudge}\n{fact}"
    )
PY

echo "✅ Fixed: relative imports in pipeline.py"
