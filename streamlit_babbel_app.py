import sys, os
sys.path.insert(0, os.path.dirname(__file__))  # Add local folder to import path
import json, os, requests
import streamlit as st

# Local utils
from babbel_core.rewrite import rewrite_tone, enforce_babbel_style
from babbel_core.rewrite_scoring import score_from_texts, get_fact_flags
from babbel_core.emotion_classifier import classify_emotion
from babbel_core.intent_classifier import classify_intent
from babbel_core.node_rules import apply_node_rules

try:
    from babbel_core.memory_tracker import log_interaction, get_recent_emotions
except Exception:
    def log_interaction(*args, **kwargs): pass
    def get_recent_emotions(n=10): return []

HARD_CODED_API_KEY = os.getenv("OPENROUTER_API_KEY","")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are Babbel. Respond concisely, concretely, and without filler. "
    "Be direct, specific, and pragmatic. Avoid hedges like 'maybe'/'just'. "
    "When helpful, provide short steps or a crisp summary. "
    "If the user asks for recent facts, be explicit about uncertainty."
)

def babbelize(txt: str) -> str:
    try:
        return enforce_babbel_style(rewrite_tone(txt)).strip()
    except Exception:
        return txt

def build_messages_with_context(history, n_pairs: int):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    tail = history[-(n_pairs*2):] if n_pairs > 0 else history
    for m in tail:
        role = m.get("role", "user")
        content = str(m.get("content", ""))[:4000]
        if role not in ("user", "assistant", "system"):
            role = "user"
        msgs.append({"role": role, "content": content})
    return msgs

def call_openrouter(model: str, temperature: float, messages):
    headers = {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Core (Streamlit)",
        "HTTP-Referer": "http://localhost:8501/",
    }
    payload = {"model": model, "messages": messages, "temperature": temperature}
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = {"error": resp.text}
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {detail}")
    data = resp.json()
    return data["choices"][0]["message"]["content"]

# ================= UI =================
st.set_page_config(page_title="Babbel Core — Streamlit (Overlays)", page_icon="🧠", layout="centered")
st.title("🧠 Babbel Core — Streamlit + Overlays")
st.caption("Message-level scoring • Node influence • Fact flags • Memory heatmap • Inline rewrite view")

# Sidebar
st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns (last N exchanges)", 1, 30, 10, 1)
use_babbel_style = st.sidebar.checkbox("Apply Babbel style", value=True)
show_context_preview = st.sidebar.checkbox("Show context preview", value=False)

st.sidebar.markdown("---")
st.sidebar.header("Overlays")
show_overlays = st.sidebar.checkbox("Enable overlays", value=True)
expand_overlays = st.sidebar.checkbox("Expand overlays by default", value=True)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()
with col2:
    if st.button("Seed greeting"):
        st.session_state.setdefault("messages", []).append({"role": "assistant", "content": "Hi—how can I help?"})
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🧭 Emotional Trajectory")
recent = get_recent_emotions(10)
st.sidebar.write(", ".join(recent[-10:]) if recent else "No history yet.")

# History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message…")

if prompt:
    # user turn
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # build context & call model
    messages_for_api = build_messages_with_context(st.session_state.messages, context_turns)
    if show_context_preview:
        st.expander("Context preview").json(messages_for_api)

    try:
        llm_text = call_openrouter(model, temperature, messages_for_api)
    except Exception as e:
        llm_text = f"⚠️ Error: {e}"

    assistant_text = babbelize(llm_text) if use_babbel_style else llm_text

    # assistant turn
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        # 🔒 Force full Babbel rewrite, always
        from babbel_core.emotion_classifier import classify_emotion
        from babbel_core.intent_classifier import classify_intent
        from babbel_core.node_rules import apply_node_rules
        from babbel_core.rewrite import rewrite_tone, enforce_babbel_style
        emo = classify_emotion(prompt)
        intent = classify_intent(prompt)
        node_out = apply_node_rules(prompt, emo, intent)
        assistant_text = enforce_babbel_style(rewrite_tone(node_out)).strip()
        st.markdown(assistant_text)

        if show_overlays:
            # Compute overlays
            emo = classify_emotion(prompt)
            intent = classify_intent(prompt)
            scores = score_from_texts(prompt, llm_text, assistant_text)
            flags = get_fact_flags(prompt)

            with st.expander("🔎 Why Babbel rewrote this", expanded=expand_overlays):
                st.markdown(f"**Rewrite confidence:** `{scores['rewrite_confidence']}`")
                st.progress(min(1.0, max(0.0, scores['rewrite_confidence'])))

                st.markdown(f"**Detected emotion:** `{emo}` • **Detected intent:** `{intent}`")
                st.markdown(f"**Node nudge:** {apply_node_rules(prompt, emo, intent)}")

                st.markdown("**Fact-check flags:** " + (", ".join(flags) if flags else "_none_"))

                # Inline view
                st.markdown("**Inline view — user → rewrite**")
                c1, c2 = st.columns(2)
                with c1:
                    st.caption("User input")
                    st.code(scores["inline"]["user"])
                with c2:
                    st.caption("Babbel rewrite")
                    st.code(scores["inline"]["rewrite"])

                # Memory heatmap (simple bars)
                heat = scores.get("memory_heatmap") or []
                if heat:
                    st.markdown("**Memory contribution (recent emotions)**")
                    for cell in heat:
                        st.write(f"{cell['label']}: {int(cell['weight']*100)}%")
                        st.progress(min(1.0, max(0.0, cell['weight'])))

    # log interaction
    try:
        log_interaction(prompt, classify_emotion(prompt), classify_intent(prompt), "openrouter", assistant_text)
    except Exception:
        pass

    # refresh sidebar
    st.sidebar.subheader("Latest trajectory")
    try:
        st.sidebar.write(", ".join(get_recent_emotions(5)))
    except Exception:
        pass

st.markdown("""
---
**Notes**
- Overlays are computed locally against the model output and Babbelized rewrite.
- Confidence is heuristic (edit distance + style improvements ± length sanity).
""")
