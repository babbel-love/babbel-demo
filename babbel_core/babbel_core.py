from babbel_core.pipeline import run_babbel_loop

if __name__ == "__main__":
    print("Babbel Brain Core started.")
    while True:
        try:
            run_babbel_loop()
        except KeyboardInterrupt:
            print("\nExiting Babbel Core.")
            break
        except Exception as e:
            print(f"Error: {e}")
