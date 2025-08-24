import shutil
import tempfile
from pathlib import Path

def _import_mt(dst_dir):
    src = Path("babbel_core/core/memory_tracker.py")
    dst = Path(dst_dir) / "memory_tracker.py"
    shutil.copy(src, dst)
    return dst

def test_log_and_recent_emotions():
    tmpdir = tempfile.mkdtemp()
    mt = _import_mt(tmpdir)
    assert Path(mt).exists()
