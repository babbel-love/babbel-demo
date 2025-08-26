#!/bin/bash
set -e
cd Babbel_Official
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed \
  --name "BabbelCore" \
  babbel_core/streamlit_babbel_app.py
echo "✅ Windows build complete: dist/BabbelCore.exe"
