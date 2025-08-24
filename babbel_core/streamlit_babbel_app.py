import os
import streamlit as st

# Import Babbel engine pieces via robust shim (works locally & in Cloud)
from _import_shim import run_pipeline, rewrite_tone, enforce_babbel_style

st.set_page_config(page_title="Babbel GUI", page_icon="🧠", layout="centered")
st.title("🧠 Babbel — Core GUI")

# Optional: show key status
api_key = os.getenv("OPENROUTER_API_KEY", "")
st.caption("OpenRouter key loaded: " + ("✅" if bool(api_key) else "⚠️ missing"))

with st.form("babbel_form", clear_on_submit=False):
    user = st.text_area("Say something to Babbel:", height=120, placeholder="I feel stuck…")
    submitted = st.form_submit_button("Run Babbel")

if submitted and user.strip():
    with st.spinner("Thinking…"):
        out = run_pipeline(user.strip())

    # Safe fallbacks for different pipeline return shapes
    final_text = (
        out.get("final_text")
        or out.get("text")
        or str(out)
    )
    st.subheader("Reply")
    st.write(final_text)

    meta = out.get("metadata") or {}
    ux = out.get("ux") or {}

    if meta:
        st.subheader("Metadata")
        st.json(meta)
    if ux:
        st.subheader("UX")
        st.json(ux)

    # Show enforced Babbel tone preview
    try:
        styled = enforce_babbel_style(rewrite_tone(final_text)).strip()
        if styled and styled != final_text:
            st.subheader("Babbel Style (enforced)")
            st.write(styled)
    except Exception:
        pass
