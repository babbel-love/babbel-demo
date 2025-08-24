import os, unittest
from babbel_core.core.orchestrator import process_message

class TestOrchestratorUX(unittest.TestCase):
    def test_ux_block_present(self):
        os.environ["BABBEL_CULTURE_SHIFT"] = "1"
        os.environ["BABBEL_TARGET_CULTURE"] = "jp"
        out = process_message("I'm a bit anxious. What should I do?")
        self.assertIn("ux", out)
        self.assertIn("reflection", out["ux"])
        self.assertIsInstance(out["ux"]["choices"], list)
        self.assertIn("style_profile", out["ux"])
        os.environ.pop("BABBEL_CULTURE_SHIFT", None)
        os.environ.pop("BABBEL_TARGET_CULTURE", None)

if __name__ == "__main__":
    unittest.main()
