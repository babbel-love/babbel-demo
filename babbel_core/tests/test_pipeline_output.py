import unittest
from babbel_core.core.pipeline import run_pipeline

class TestPipelineOutput(unittest.TestCase):
    def test_pipeline_structure(self):
        user_input = "I feel stuck and unsure how to begin."
        out = run_pipeline(user_input)
        self.assertIn("final_text", out)
        self.assertIn("metadata", out)
        self.assertIn("ux", out)
        self.assertIn("emotion", out["metadata"])
        self.assertIn("choices", out["ux"])
        self.assertIsInstance(out["ux"]["choices"], list)

if __name__ == "__main__":
    unittest.main()
