import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, tempfile, json
from self_awareness import grep, find_symbols, describe_project

def test_grep_finds_this_test_file():
    hits = grep(r"test_self_awareness", ".")
    assert any("test_self_awareness.py" in h["file"] for h in hits)

def test_find_symbols_detects_function_like_names(tmp_path):
    p = tmp_path / "mod.py"
    p.write_text("def cool_symbol():\\n    return 1\\n", encoding="utf-8")
    hits = find_symbols("cool_symbol", str(tmp_path))
    assert any(h["file"].endswith("mod.py") for h in hits)

def test_describe_project_counts_extensions(tmp_path):
    (tmp_path / "a.py").write_text("print(1)", encoding="utf-8")
    (tmp_path / "b.json").write_text("{}", encoding="utf-8")
    summary = describe_project(str(tmp_path))
    assert summary.get(".py", 0) >= 1 and summary.get(".json", 0) >= 1
