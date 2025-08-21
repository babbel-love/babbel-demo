# Babbel Engine Bootstrap Complete

To run Babbel in CLI mode:
    ./run_babbel.sh

To run tests:
    ./run_tests.sh

To install dependencies:
    python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

To format code:
    black .
    isort .

All protocol guards, prompt builders, and fallback blocks are pre-installed.
You're now running a hardened override engine with GPT decontamination.

