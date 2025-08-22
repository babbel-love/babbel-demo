from babbel.gui.interface_retry import BabbelGUIRetry
def test_send_user_input_success():
    gui = BabbelGUIRetry()
    reply = gui.send_user_input("Hello world")
    assert reply == "Processed with anchored memory and retry check."
    assert len(gui.session_history) == 1
    assert gui.get_last_emotion() == "Neutral"
    assert gui.get_last_node() == "None"
def test_send_user_input_failure(monkeypatch):
    gui = BabbelGUIRetry()
    def fail_prompt(_):
        return [{"role": "system", "content": "As an AI language model, I can help."}]
    from babbel.core import prompt_builder
    monkeypatch.setattr(prompt_builder, "build_messages", fail_prompt)
    reply = gui.send_user_input("Trigger retry")
    assert "Protocol retry failed" in reply
