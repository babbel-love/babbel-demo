from babbel.core.protocol_retry import BabbelEngineRetry
import pytest

def test_send_retries_on_protocol_violation(monkeypatch):
    engine = BabbelEngineRetry()
    def bad_prompt(_):
        return [{"role": "system", "content": "As an AI language model, I can help."}]
    from babbel.core import prompt_builder
    monkeypatch.setattr(prompt_builder, "build_messages", bad_prompt)
    with pytest.raises(RuntimeError, match="Protocol retry failed"):
        engine.send("test retry", strict=True, max_retries=2)

def test_send_succeeds_with_clean_prompt():
    engine = BabbelEngineRetry()
    reply = engine.send("normal input", strict=True)
    assert reply["text"] == "Processed with anchored memory and retry check."
    assert engine.memory["anchor"] == "latest"
