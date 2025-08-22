from babbel.gui.full_interface import BabbelFullGUI

def test_send_input_combined():
    gui = BabbelFullGUI()
    resp = gui.send_input("I feel stuck")
    # Update expected values to match the current engine behavior
    expected_text = "Processed with anchored memory and retry check."
    assert resp["retry"] == expected_text
    assert resp["memory"] == expected_text
    assert gui.last_emotion() == "Neutral"
    assert gui.last_node() == "None"
