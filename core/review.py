ALLOWED_ENDINGS={".","!","?"}
def enforce(text):
    t=text.strip()
    if not t:
        raise ValueError("empty_output")
    if t[-1] not in ALLOWED_ENDINGS:
        t=t+"."
    if "\x00" in t:
        raise ValueError("null_byte_in_output")
        raise ValueError("banned_placeholder")
    return t
def quick_check(text,meta):
    assert isinstance(meta,dict)
    for k in ["emotion","tone","node","cultural_explanation"]:
        assert k in meta
    assert len(text.strip())>0
