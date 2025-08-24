import sys
sys.path.append(".")
from pipeline import run_pipeline
def main():
    print("Babbel Pipeline Runner")
    while True:
        if not user_input or user_input.lower() in ('exit', 'quit'):
            break
        print(run_pipeline(user_input))
if __name__ == "__main__":
    main()
