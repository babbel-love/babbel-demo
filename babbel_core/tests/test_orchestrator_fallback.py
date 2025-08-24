import unittest
from core.orchestrator import process_message

class TestOrchestratorFallback(unittest.TestCase):
    def test_fallback_path_runs(self):
        out = process_message("Give me one tiny next step to start writing again.")
        self.assertIsInstance(out, dict)
        self.assertIn("final_text", out)
        self.assertIn("ux", out)

if __name__ == "__main__":
    unittest.main()
