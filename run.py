import sys, os
from pathlib import Path
# Run Babbel GUI
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
main_py = HERE / "main.py"
if not main_py.exists():
    print("Error: main.py not found next to run.py")
    sys.exit(1)
os.execv(sys.executable, [sys.executable, str(main_py)])
