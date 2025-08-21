import unittest
from babbel_core.core.schema import validate_payload, to_dict

class TestSchema(unittest.TestCase):
    def test_validate_and_roundtrip(self):
        obj = {
            "trace_id": "t1",
            "guiding_line": "Do the kind thing",
            "final_text": "Okay.",
            "emotion": "sadness",
            "intent": "seek guidance",
            "notes": None,
            "tokens_used": 42,
            "timestamp_utc": "2024-01-01T00:00:00+00:00",
            "safety": {"blocked": False, "reasons": []},
            "ux": {"a": 1},
        }
        fp = validate_payload(obj)
        d = to_dict(fp)
        self.assertEqual(d["emotion"], "grief")
        self.assertIn("ux", d)

    def test_bad_timestamp(self):
        bad = {
            "trace_id":"x","guiding_line":"g","final_text":"f","emotion":"anger",
            "intent":"explore","timestamp_utc":"2020-01-01T00:00:00","safety":{"blocked":False,"reasons":[]}
        }
        with self.assertRaises(ValueError):
            validate_payload(bad)

if __name__ == "__main__":
    unittest.main()
