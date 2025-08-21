from babbel.core.engine import BabbelEngine

def run_gui_sim():
    engine = BabbelEngine()
    print('Babbel Override CLI (type exit to quit)')
    while True:
        user_input = input('You: ')
        if user_input.strip().lower() in ['exit', 'quit']:
            break
        try:
            response = engine.send(user_input, strict=True)
            print('Babbel:', response['text'])
        except Exception as e:
            print('ERROR:', e)

if __name__ == '__main__':
    run_gui_sim()

