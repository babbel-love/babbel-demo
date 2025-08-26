#!/bin/bash
set -e
cd Babbel_Official
pip install py2app create-dmg
rm -rf dist build Babbel.app
mkdir -p dist
py2applet --make-setup babbel_core/streamlit_babbel_app.py
python3 setup.py py2app
mv dist/Babbel.app dist/Babbel_Core.app
create-dmg dist/Babbel_Core.app \
  --volname "Babbel" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --app-drop-link 400 150 \
  Babbel_Core.dmg
