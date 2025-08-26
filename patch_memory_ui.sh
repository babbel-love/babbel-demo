#!/bin/bash
set -euo pipefail

APP="babbel_core/streamlit_babbel_app.py"
SESSIONS_DIR="babbel_core/sessions"
mkdir -p "$SESSIONS_DIR"

echo "🔧 Patching memory UI features into \$APP..."

cat <<'PYCODE' >> "$APP"

# === [📦 Session Save/Load] ===
import os
from thread import ConversationThread
SESSIONS_DIR = "babbel_core/sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

st.sidebar.subheader("🧵 Sessions")
session_files = sorted(f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json"))

def load_session(path):
    try:
        full_path = os.path.join(SESSIONS_DIR, path)
        return ConversationThread.load(full_path)
    except Exception:
        return None

selected_file = st.sidebar.selectbox("Load session", ["(new)"] + session_files)
if selected_file != "(new)":
    loaded = load_session(selected_file)
    if loaded:
        st.session_state.messages = loaded.messages
        st.success(f"Loaded: {selected_file}")

if st.sidebar.button("💾 Save current session"):
    thread = ConversationThread("Saved via GUI", model, temperature, context_turns)
    thread.messages = st.session_state.messages
    thread.save(SESSIONS_DIR)
    st.success("Session saved.")

# === [🔍 Emotion Search] ===
st.sidebar.subheader("🔍 Search by Emotion")
search_emotion = st.sidebar.text_input("Enter emotion (e.g. shame, fear)").lower().strip()
if search_emotion:
    matches = [m for m in st.session_state.messages if search_emotion in m.get("content", "").lower()]
    st.sidebar.write(f"{len(matches)} matches")
    if matches:
        with st.expander("Matching Messages"):
            for m in matches:
                st.markdown(f"**{m['role']}**: {m['content']}")

# === [📤 Export CSV/TXT] ===
import pandas as pd
st.sidebar.subheader("📤 Export")
def export_dataframe():
    return pd.DataFrame([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])

if st.sidebar.button("Export as CSV"):
    df = export_dataframe()
    df.to_csv("babbel_export.csv", index=False)
    st.success("Exported to babbel_export.csv")

if st.sidebar.button("Export as TXT"):
    with open("babbel_export.txt", "w", encoding="utf-8") as f:
        for m in st.session_state.messages:
            f.write(f"{m['role'].upper()}: {m['content']}\n\n")
    st.success("Exported to babbel_export.txt")

# === [🪪 Rewrite Debugger] ===
from node_rewrite_v2 import NodeRewriterV2
st.markdown("---")
with st.expander("🪪 Rewrite Debugger"):
    rewriter = NodeRewriterV2()
    test_input = st.text_area("Input to test rewrite", "Can you help with my issue?")
    if st.button("Run Rewrite Debugger"):
        output = rewriter.rewrite_node(test_input)
        st.write("Rewritten Output:")
        st.success(output)

# === [📊 Emotion Graph] ===
import matplotlib.pyplot as plt
try:
    emolist = get_recent_emotions(50)
    if emolist:
        st.sidebar.subheader("📊 Emotion Graph")
        fig, ax = plt.subplots()
        ax.plot(emolist, marker='o')
        ax.set_xticks(range(len(emolist)))
        ax.set_xticklabels(range(1, len(emolist)+1), rotation=90)
        ax.set_ylabel("Emotion")
        ax.set_title("Recent Emotion Trajectory")
        st.sidebar.pyplot(fig)
except Exception:
    st.sidebar.info("No graph data yet.")
PYCODE

echo "✅ All memory UI features added to \$APP."
