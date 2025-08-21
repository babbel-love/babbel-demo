import pytest
from babbel.core import prompt_builder, prompt_guard
from babbel.core.engine import BabbelEngine

def test_validate_node_context_accepts_clean_prompt():
    messages = prompt_builder.build_messages('I feel stuck in collapse.')
    prompt_guard.validate_node_context(messages)

def test_validate_node_context_rejects_gpt_phrases():
    messages = [{'role': 'system', 'content': 'As an AI language model, I can help. Node: Compliance'}]
    with pytest.raises(RuntimeError, match='GPT-style fallback language detected'):
        prompt_guard.validate_node_context(messages)

def test_engine_send_rejects_bad_prompt():
    engine = BabbelEngine()
    def fake_prompt(_): return [{'role': 'system', 'content': 'You are a helpful assistant. Node: Despair'}]
    prompt_builder.build_messages = fake_prompt
    with pytest.raises(RuntimeError):
        engine.send('test', strict=True)

