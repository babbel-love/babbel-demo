Babbel GUI — Quick Start
========================

Mac/Linux:
  1) Open Terminal.
  2) cd to this folder.
  3) Run:    ./run_mac.sh

Windows (PowerShell):
  1) Right-click Start → Windows PowerShell.
  2) cd to this folder.
  3) Run:    ./run_windows.ps1

If you already have a venv, you can also just run:
  python run.py

Notes:
- This script creates a local virtualenv in .venv and installs any detected dependencies from requirements.txt.
- If the app uses additional services (OpenRouter API keys, etc.), set them as environment variables before launching.
- If PyQt6 isn't installed by default on your system, it will be installed into the venv.
