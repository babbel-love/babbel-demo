import streamlit as st
import re
import json
from datetime import datetime

FACT_FLAG_WORDS = ("latest", "today", "as of", "currently", "expected", "estimated", "about", "roughly")

def rewrite_tone(text):
    out = text
    for pat in [r"\bjust\b", r"\bmaybe\b", r"\bperhaps\b", r"\bi think\b", r"\bit seems\b", r"\bi feel like\b", r"\bkinda\b", r"\bsort of\b"]:
        out = re.sub(pat, "", out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out).strip()

def enforce_babbel_style(text):
    for pat, repl in [(r"\bthere (is|are)\b\s*", ""), (r"\bit is important to note that\b\s*", ""), (r"\bshould\b", "must"), (r"\butilize\b", "use"), (r"\bcan be\b\s+(\w+)\s+as\b", r"is \1")]:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", text).strip()

def classify_emotion(text):
    t = text.lower()
    if any(w in t for w in ["worthless", "disgust", "ashamed"]): return "shame"
    if any(w in t for w in ["sad", "heartbroken", "loss"]): return "grief"
    if any(w in t for w in ["angry", "rage", "fed up"]): return "anger"
    if any(w in t for w in ["curious", "what if", "open to"]): return "wonder"
    if any(w in t for w in ["scared", "anxious", "afraid"]): return "fear"
    return "mixed"

def classify_intent(text):
    t = text.lower()
    if any(w in t for w in ["what should", "need advice", "help me"]): return "seek guidance"
    if any(w in t for w in ["i'm sorry", "it's my fault", "i feel guilty"]): return "confession"
    if any(w in t for w in ["you never", "why would you", "always do this"]): return "protest"
    if any(w in t for w in ["why", "what does it mean", "what's wrong with me"]): return "search for meaning"
    return "explore"

def apply_node_rules(text, emotion, intent):
    if emotion == "shame": return "You’re holding something unbearable — not because it’s true, but because it feels that way."
    if emotion == "grief" and intent == "search for meaning": return "Grief isn’t just pain — it’s proof that something mattered. We’ll stay with that."
    if emotion == "anger": return "That edge in your voice? It matters. Let’s hear it without trying to tame it."
    if emotion == "wonder": return "There’s something alive in that wondering. Let’s not rush to explain it away."
    if emotion == "fear" and intent == "seek guidance": return "I’m with you. We’ll face this carefully — not quickly."
    if intent == "confession": return "You’re not asking for advice. You’re asking if it’s still okay to be seen. It is."
    return "Let’s slow this down together and see what’s really here."

def log_interaction(user_input, emotion, intent, raw_reply, final_reply):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "emotion": emotion,
        "intent": intent,
        "raw_reply": raw_reply,
        "final_reply": final_reply
    }
    try:
        with open("memory_log.json", "r") as f:
            data = json.load(f)
    except Exception:
        data = []
    data.append(entry)
    with open("memory_log.json", "w") as f:
        json.dump(data[-100:], f, indent=2)

def get_recent_emotions(n=10):
    try:
        with open("memory_log.json", "r") as f:
            logs = json.load(f)
        return [x["emotion"] for x in logs[-n:] if "emotion" in x]
    except Exception:
        return []

def run_pipeline(prompt):
    prompt = prompt.strip()
    if not prompt:
        return {"text": "No input provided.", "metadata": {}}
    emotion = classify_emotion(prompt)
    intent = classify_intent(prompt)
    rewrite = apply_node_rules(prompt, emotion, intent)
    toned = rewrite_tone(rewrite)
    styled = enforce_babbel_style(toned)
    return {
        "text": styled,
        "metadata": {
            "emotion": emotion,
            "intent": intent,
            "node": "computed"
        }
    }

st.set_page_config(page_title="Babbel", page_icon="🧠", layout="centered")
st.title("🧠 Babbel (Local)")
st.caption("No external calls. Fully internal tone + memory logic.")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("Session")
if st.sidebar.button("Clear chat"):
    st.session_state.pop("messages", None)
    st.rerun()

st.sidebar.header("Emotion Log")
st.sidebar.write(", ".join(get_recent_emotions()))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    out = run_pipeline(prompt)
    reply = out["text"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    try:
        log_interaction(prompt, out["metadata"].get("emotion", "n/a"), out["metadata"].get("intent", "n/a"), "pipeline", reply)
    except Exception:
