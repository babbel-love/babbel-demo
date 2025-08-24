from babbel_core import session_controls

def test_reset_session_empties_state():
    session = session_controls.reset_session()
    assert session["messages"] == []
    assert session["memory"] == {}
    assert session["thread_id"] is None
