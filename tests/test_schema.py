import pytest
from babbel.core.schema import validate_timestamp

def test_bad_timestamp():
    with pytest.raises(ValueError):
        validate_timestamp("not-a-valid-time")
