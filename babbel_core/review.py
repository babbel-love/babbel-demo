from babbel_core.rewrite import rewrite_tone, enforce_babbel_style

def run_review_stage(draft: str) -> dict:
    print("[Review Stage] Reviewing draft and applying style enforcement.")
    toned = rewrite_tone(draft)
    styled = enforce_babbel_style(toned)
    print("[Review Stage] Quick check: Tone strengthened, Babbel style enforced.")
    return {
        "reviewed_text": styled,
        "quick_check": "Tone strengthened. Style rewritten to match Babbel voice."
    }
