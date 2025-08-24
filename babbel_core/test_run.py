from core.engine import BabbelEngine

if __name__ == "__main__":
    engine = BabbelEngine()
    while True:
        try:
            if not user_input:
                continue
            out = engine.send(user_input)
            print(f"Babbel: {out['text']}")
        except KeyboardInterrupt:
            print("\n[Exited]")
            break
        except Exception as e:
            print(f"[Error] {e}")
