import unittest
from core.culture_shift import apply_and_explain, _soften_imperatives

class TestCultureShift(unittest.TestCase):
    def test_soften(self):
        adj, expl = apply_and_explain("Pick one option.\nAsk a friend.", "jp")
        self.assertTrue("softened" in expl.lower() or "invitational" in expl.lower())
        self.assertNotEqual(adj, "")
        # grammar check: no "Consider to"
        softened = _soften_imperatives("Pick one option.")
        self.assertIn("Consider one option.", softened)

    def test_unknown(self):
        adj, expl = apply_and_explain("Do one thing.", "xx")
        self.assertIn("left unchanged", expl.lower())

if __name__ == "__main__":
    unittest.main()
