DEFAULT_MODEL = "babbel-local/deterministic"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MEMORY_TURNS = 10

def get_config():
    return {
        "model": DEFAULT_MODEL,
        "temperature": DEFAULT_TEMPERATURE,
        "memory_turns": DEFAULT_MEMORY_TURNS
    }
