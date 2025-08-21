Build a macOS .dmg for Babbel
=============================

Requirements (on a Mac):
- Python 3.9+ preinstalled
- Command Line Tools (Xcode CLT)
- Optional: Homebrew `create-dmg` for a nicer DMG (otherwise we use `hdiutil`)

Steps:
1) Open Terminal and cd into this folder.
2) Run:
   chmod +x create_dmg.sh
   ./create_dmg.sh

What it does:
- Creates/uses a `.venv`
- Installs `pyinstaller` and app requirements
- Builds `dist/Babbel.app`
- Creates `Babbel.dmg` (pretty if `create-dmg` is available)

Customization:
- Place a custom icon at `resources/app.icns` (optional)
- Place a DMG background at `resources/dmg_background.png` (optional)

Signing/Notarization (optional, manual):
- Once you have `Babbel.app`, you can codesign & notarize before DMG creation.
