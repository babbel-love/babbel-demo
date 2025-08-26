from babbel_core.engine import BabbelEngine

def test_engine_instantiates():
    engine = BabbelEngine()
    assert engine is not None
