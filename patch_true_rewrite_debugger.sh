#!/bin/bash
set -euo pipefail

APP="babbel_core/streamlit_babbel_app.py"

echo "🔧 Replacing dummy rewrite debugger with full node-aware version..."

cat <<'PY' >> "$APP"

# === [🧠 True Rewrite Debugger — Node-Aware] ===
from emotion_classifier import classify_emotion
from intent_classifier import classify_intent
from node_rules import apply_node_rules
from rewrite import rewrite_tone, enforce_babbel_style

st.markdown("---")
with st.expander("🧠 Node-Aware Rewrite Debugger"):
    test_input = st.text_area("Try anything emotionally raw...", "I feel worthless and broken.")
    if st.button("Run Real Babbel Debugger"):
        emotion = classify_emotion(test_input)
        intent = classify_intent(test_input)
        node_text = apply_node_rules(test_input, emotion, intent)
        styled_text = enforce_babbel_style(rewrite_tone(node_text)).strip()

        st.markdown(f"**Detected Emotion:** `{emotion}`")
        st.markdown(f"**Detected Intent:** `{intent}`")

        st.markdown("**🔁 Babbel Rewrite:**")
        st.success(styled_text)

        st.markdown("**💡 Explanation:**")
        if emotion == "shame":
            st.info("This rewrite is grounded in the assumption that shame often distorts truth into unbearable self-judgment. Babbel gently reframes the emotion without invalidating it.")
        elif emotion == "grief":
            st.info("Grief isn't bypassed here — it's honored. The rewrite respects what was lost while inviting depth.")
        elif intent == "confession":
            st.info("Rather than offer advice, Babbel recognizes the need to feel seen. It offers presence instead of solutions.")
        else:
            st.info("The rewrite slows things down, offering space rather than rushing to explain or fix.")
PY

echo "✅ True node-aware debugger injected."
