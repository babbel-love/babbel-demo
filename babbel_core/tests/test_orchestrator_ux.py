from babbel_core.engine import BabbelEngine
import unittest

class TestOrchestratorUX(unittest.TestCase):
    def test_ux_block_present(self):
        eng = BabbelEngine()
        out = eng.send("I'm a bit anxious. What should I do?")
        assert "ux" in out
        assert "choices" in out["ux"]
        assert isinstance(out["ux"]["choices"], list)
