import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline import run_pipeline

def main():
    print("✅ Babbel Test Pipeline: Running manual prompt loop")
    print("Type a message, or 'exit' to quit.\n")
    while True:
        user_input = input("Prompt> ").strip()
        if not user_input or user_input.lower() in ("exit", "quit"):
            break
        response = run_pipeline(user_input)
        print("\n🧠 Babbel Final Output:\n")
        print(response)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
