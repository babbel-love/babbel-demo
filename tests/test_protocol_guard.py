from babbel.core import protocol_guard
import pytest

def test_rejects_gpt_fallback_phrases():
    messages = [{"role": "system", "content": "As an AI language model, I can help."}]
    with pytest.raises(RuntimeError):
        protocol_guard.enforce_protocol_guard(messages)

def test_accepts_clean_protocol_message():
    messages = [{"role": "system", "content": "Running Babbel Protocols. Current node: Collapse → Agency."}]
    protocol_guard.enforce_protocol_guard(messages)  # Should not raise
