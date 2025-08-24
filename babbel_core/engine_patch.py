def patch_engine_response(response: dict) -> dict:
    response["metadata"]["patched"] = True
    return response
