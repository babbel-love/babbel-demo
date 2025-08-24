from pipeline import run_babbel_loop

if __name__ == "__main__":
    while True:
        try:
            run_babbel_loop()
        except KeyboardInterrupt:
            break
        except Exception as e:
