import unittest
from core.hx_engine import build_extras, compose_brief

class TestHXEngine(unittest.TestCase):
    def test_build_and_compose(self):
        ex = build_extras("I feel anxious", "fear", "seek guidance", "warm_coach")
        self.assertIn("reflection", ex)
        self.assertGreaterEqual(len(ex.get("choices", [])), 2)
        txt = compose_brief(ex, max_items=2)
        self.assertTrue(len(txt.strip()) > 0)
        self.assertLessEqual(len(txt.splitlines()), 6)

if __name__ == "__main__":
    unittest.main()
