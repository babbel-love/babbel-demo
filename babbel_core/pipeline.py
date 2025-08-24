import re
from rewrite import rewrite_tone, enforce_babbel_style

FACT_FLAG_WORDS = ("latest","today","as of","currently","expected","estimated","about","roughly")

def _choose_goal(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ("how ","how do i","how to","how should")): return "method"
    if "why" in t: return "causes"
    if "when" in t or "date" in t: return "time"
    if any(k in t for k in ("latest","today","currently")): return "current fact"
    return "general"

def run_pipeline(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt: return "No input."
    goal = _choose_goal(prompt)
    flags = [w for w in FACT_FLAG_WORDS if w in prompt.lower()]
    if re.search(r"\d", prompt): flags.append("number")
    flags = sorted(set(flags))
    fact = f"[Fact-check] Output requires validation: {', '.join(flags)}." if flags else "[Fact-check] No factual red flags detected."
    final_text = enforce_babbel_style(rewrite_tone(prompt)).strip()
    return (
        f"Final Answer: {final_text}\n\n"
        "Quick check:\n"
        f"- Style: Babbel voice enforced\n- Fact flags: {', '.join(flags) if flags else 'none'}\n- Tone: direct, concise\n\n"
        "— Traces —\n"
        f"Plan: Goal: {goal}\n"
        "Draft: Give a clear, direct answer. If steps help, list them. Name trade-offs briefly. Avoid filler.\n"
        "Review: Babbel voice: concise, direct, specific. Remove hedges and weak phrasing.\n"
        f"{fact}"
    )

def run_babbel_loop():
    try:
        user_input = input("\n🗣️  You: ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not user_input:
        print("⚠️  Empty input."); return
    print(f"\n🤖 Babbel: {run_pipeline(user_input)}")
