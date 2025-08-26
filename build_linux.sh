#!/bin/bash
set -e
cd Babbel_Official
pip install pyinstaller
pyinstaller --noconfirm --onefile \
  --name "BabbelCore" \
  babbel_core/streamlit_babbel_app.py
echo "✅ Linux build complete: dist/BabbelCore"
echo "To make AppImage, install appimagetool and run: appimagetool dist/"
