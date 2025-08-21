import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from babbel.core.orchestrator import process_message

if __name__ == "__main__":
    sample = "I feel like there's no point trying anymore"
    history = []
    result = process_message(sample, history)

    print("---- BABBEL RESPONSE ----")
    print(result['text'])
    print("\\n---- METADATA ----")
    print(result['metadata'])
    print("\\n---- SCORES ----")
    print(result['scores'])
    print("\\n---- CULTURAL NOTE ----")
    print(result['cultural_note'])
    print("\\n---- EMOTION BAR ----")
    print(result['emotion_bar'])
