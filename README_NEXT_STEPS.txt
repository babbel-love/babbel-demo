Welcome to the Babbel Packaging Tool.

▶ Drop this folder anywhere on your machine.
▶ Open Terminal in this folder.
▶ Run the appropriate script:

  bash build_mac.sh    # macOS .app and .dmg
  bash build_win.sh    # Windows .exe
  bash build_linux.sh  # Linux .AppImage

Make sure Python 3.11+ is installed and you’ve run:

  pip install -r requirements.txt

Before launching the app, export your API key:

  export OPENROUTER_API_KEY="sk-or-..."

App lives in: Babbel_Official/babbel_core/streamlit_babbel_app.py

Next steps are inside Babbel_Official/README_NEXT_STEPS.txt
