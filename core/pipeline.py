import re
from babbel_core.core import rewrite, review

FACT_FLAG_WORDS = ("latest", "today", "as of", "currently", "expected", "estimated", "about", "roughly")

def _choose_goal(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ("how ", "how do i", "how to", "how should")):
        return "method"
    if "why" in t:
        return "causes"
    if "when" in t or "date" in t:
        return "time"
    if any(k in t for k in ("latest", "today", "currently")):
        return "current fact"
    return "general"

def run_pipeline(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return "No input."
    goal = _choose_goal(prompt)
    plan = f"Goal: {goal}"
    draft = (
        "Give a clear, direct answer. If steps help, list them. "
        "Name trade-offs briefly. Avoid filler."
    )
    review_note = "Babbel voice: concise, direct, specific. Remove hedges and weak phrasing."
    flags = [w for w in FACT_FLAG_WORDS if w in prompt.lower()]
    if re.search(r"\d", prompt):
        flags.append("number")
    flags = sorted(set(flags))
    fact = (
        f"[Fact-check] Output requires validation: {', '.join(flags)}."
        if flags else "[Fact-check] No factual red flags detected."
    )
    final_text = rewrite.enforce_babbel_style(rewrite.rewrite_tone(f"{prompt}")).strip()
    result = (
        f"Final Answer: {final_text}\n\n"
        "Quick check:\n"
        f"- Style: Babbel voice enforced\n- Fact flags: {', '.join(flags) if flags else 'none'}\n- Tone: direct, concise\n\n"
        "— Traces —\n"
        f"Plan: {plan}\nDraft: {draft}\nReview: {review_note}\n{fact}"
    )
    return result

def run_babbel_loop():
    try:
        user_input = input("\n🗣️  You: ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not user_input:
        print("⚠️  Empty input.")
        return
    output = run_pipeline(user_input)
    print(f"\n🤖 Babbel: {output}")
