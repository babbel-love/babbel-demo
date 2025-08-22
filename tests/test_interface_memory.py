from babbel.gui.interface_memory import BabbelGUIInterface
def test_send_user_input_updates_history():
    gui = BabbelGUIInterface()
    reply = gui.send_user_input("I feel lost")
    assert reply == "Processed with anchored memory and retry check."
    assert len(gui.session_history) == 1
    assert gui.get_last_emotion() == "Neutral"
    assert gui.get_last_node() == "None"
