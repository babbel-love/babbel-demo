#!/bin/bash
set -euo pipefail

APP="babbel_core/streamlit_babbel_app.py"
SESSIONS_DIR="babbel_core/sessions"

echo "🔧 Re-patching autosave + autoload for macOS-compatible sed..."

# Append autosave function to bottom of file
cat <<'PY' >> "$APP"

# === [🧷 Autosave every turn] ===
def autosave_session():
    thread = ConversationThread("AutoSaved", model, temperature, context_turns)
    thread.messages = st.session_state.messages
    thread.save(SESSIONS_DIR)

# Run autosave after assistant reply
try:
    autosave_session()
except Exception:
    pass
PY

# Patch auto-load logic at startup
TMP_PATCH=".autoload_patch.py"

cat <<'PYLOAD' > "$TMP_PATCH"
import glob
session_files = sorted(glob.glob("babbel_core/sessions/*.json"), key=os.path.getmtime, reverse=True)
if session_files:
    try:
        last_thread = ConversationThread.load(session_files[0])
        st.session_state["messages"] = last_thread.messages
        st.toast("🔄 Loaded latest session")
    except Exception:
        st.session_state["messages"] = []
else:
    st.session_state["messages"] = []
PYLOAD

# Insert into streamlit_babbel_app.py after the line: if "messages" not in st.session_state:
awk '
/if \("messages" not in st.session_state\):/ {
  print
  while ((getline line < "'"$TMP_PATCH"'") > 0) print "    " line
  next
}
{ print }
' "$APP" > "$APP.patched" && mv "$APP.patched" "$APP"

rm -f "$TMP_PATCH"

echo "✅ Autosave + autoload logic successfully patched into $APP"
