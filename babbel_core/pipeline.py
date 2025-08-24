def run_pipeline(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return "No input."
    return f"Final Answer: {prompt}"

def run_babbel_loop():
    try:
        user_input = input("\n🗣️  You: ").strip()
        if not user_input:
            print("⚠️  Empty input.")
            return
        output = run_pipeline(user_input)
        print(f"\n🤖 Babbel: {output}")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
