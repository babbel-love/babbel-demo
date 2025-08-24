from babbel_core.core.pipeline import run_pipeline

def main():
    print("Babbel Pipeline Runner (no GUI)")
    print("-" * 40)
    while True:
        user_input = input("Prompt> ").strip()
        if not user_input or user_input.lower() in ('exit', 'quit'):
            break
        print("\nRunning pipeline...\n")
        response = run_pipeline(user_input)
        print("\n--- FINAL OUTPUT ---")
        print(response)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
