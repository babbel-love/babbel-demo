from babbel_core.engine import process_message

REQUIRED_KEYS = {"final_text", "metadata"}
OPTIONAL_KEYS = {"emotion_bar", "session_emotions"}

def check_case(**flags):
    res = process_message(text="Hello test", **flags)
    missing = REQUIRED_KEYS - set(res.keys())
    extra   = set(res.keys()) - (REQUIRED_KEYS | OPTIONAL_KEYS)
    ok = not missing and not extra
    label = "✅ PASS" if ok else "❌ FAIL"
    print(label, flags)
    if missing: print("   Missing:", missing)
    if extra:   print("   Unexpected:", extra)

cases = [
]

for c in cases:
    check_case(**c)
