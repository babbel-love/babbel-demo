from core.thread import ConversationThread
import tempfile
from pathlib import Path

def test_export_saving(tmp_path):
    thread = ConversationThread("test", "openrouter/auto")
    file_path = tmp_path / "export.json"
    thread.save(file_path)
    assert file_path.exists()
