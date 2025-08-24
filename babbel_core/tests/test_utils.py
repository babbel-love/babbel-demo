import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from core.utils import slugify, safe_read_json, safe_write_json
import tempfile, os, json

def test_slugify_basic():
    assert slugify("Hello World!") == "hello-world"
    assert slugify("  A   B   C  ") == "a-b-c"

def test_safe_json_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "x.json")
        data = {"a":1,"b":[2,3]}
        safe_write_json(p, data)
        back = safe_read_json(p, {})
        assert back == data
