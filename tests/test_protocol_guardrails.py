import pytest
from babbel.core import prompt_guard
from babbel.core import prompt_builder
def test_engine_send_rejects_bad_prompt(monkeypatch):
    def fake_prompt(_):
        return [{"role": "system", "content": "As an AI language model, I can help."}]
    monkeypatch.setattr(prompt_builder, "build_messages", fake_prompt)
    messages = fake_prompt("test")
    with pytest.raises(RuntimeError):
        prompt_guard.validate_node_context(messages)
