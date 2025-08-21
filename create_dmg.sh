#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${APP_NAME:-Babbel}"
ENTRY="${ENTRY:-main.py}"
ICON_PATH="${ICON_PATH:-resources/app.icns}"
DMG_BG="${DMG_BG:-resources/dmg_background.png}"

# logging helpers
log(){ printf "\033[1;34m[INFO]\033[0m %s\n" "$*"; }
warn(){ printf "\033[1;33m[WARN]\033[0m %s\n" "$*"; }
err(){ printf "\033[1;31m[ERR ]\033[0m %s\n" "$*"; }
run(){ if [[ "${DRYRUN:-0}" == "1" ]]; then echo "+ $*"; else eval "$@"; fi }

trap 'err "Build failed on line $LINENO"; exit 1' ERR

UNAME="$(uname -s || true)"
if [[ "${DRYRUN:-0}" != "1" ]]; then
  if [[ "$UNAME" != "Darwin" ]]; then
    err "This script must be run on macOS (Darwin). Detected: $UNAME"
    exit 1
  fi
else
  warn "DRYRUN mode: not executing macOS-specific tools; just validating steps."
fi

log "Creating/activating venv (.venv)"
if [[ ! -d ".venv" ]]; then
  run "python3 -m venv .venv"
fi
# shellcheck disable=SC1091
run "source .venv/bin/activate"

log "Upgrading pip, wheel, setuptools"
run "python -m pip install --upgrade pip wheel setuptools"

log "Installing PyInstaller and project requirements"
run "pip install pyinstaller"
if [[ -s requirements.txt ]]; then
  run "pip install -r requirements.txt"
else
  warn "requirements.txt is empty or missing; continuing."
fi

# Build .app with PyInstaller (macOS only)
PYI_ARGS=(--windowed --noconfirm --name "$APP_NAME")
if [[ -f "$ICON_PATH" ]]; then
  PYI_ARGS+=(--icon "$ICON_PATH")
else
  warn "Icon not found at '$ICON_PATH' — continuing without app icon."
fi

log "Building app with PyInstaller → dist/${APP_NAME}.app"
run "pyinstaller \"${PYI_ARGS[@]}\" \"$ENTRY\""

APP_BUNDLE="dist/${APP_NAME}.app"
if [[ "${DRYRUN:-0}" != "1" ]]; then
  if [[ ! -d "$APP_BUNDLE" ]]; then
    err "App bundle not found at $APP_BUNDLE. Check PyInstaller logs above."
    exit 1
  fi
fi

DMG_PATH="${APP_NAME}.dmg"

# Prefer create-dmg if present for a polished DMG; fall back to hdiutil
if command -v create-dmg >/dev/null 2>&1; then
  log "Using create-dmg to build a styled DMG → $DMG_PATH"
  CD_ARGS=(--volname "$APP_NAME" --window-size 540 380 --icon-size 128 --app-drop-link 420 210)
  if [[ -f "$DMG_BG" ]]; then
    CD_ARGS+=(--background "$DMG_BG")
  else
    warn "DMG background not found at '$DMG_BG' — continuing with default."
  fi
  CD_ARGS+=("$DMG_PATH" "dist/")
  run "create-dmg \"${CD_ARGS[@]}\""
else
  log "create-dmg not found; using hdiutil UDZO instead → $DMG_PATH"
  run "hdiutil create -volname \"$APP_NAME\" -srcfolder \"$APP_BUNDLE\" -ov -format UDZO \"$DMG_PATH\""
fi

log "Done. Output DMG at: $DMG_PATH"
