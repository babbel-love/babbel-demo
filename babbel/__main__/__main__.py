from babbel.core.engine import BabbelEngine

def main():
    engine = BabbelEngine()
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit']:
            break
        response = engine.send(user_input, strict=True)
        print('Babbel:', response['text'])

if __name__ == '__main__':
    main()

