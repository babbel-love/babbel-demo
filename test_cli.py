
import os, json
from babbel_core.core.orchestrator import process_message
os.environ["BABBEL_CULTURE_SHIFT"] = "1"
os.environ["BABBEL_TARGET_CULTURE"] = "jp"
os.environ["BABBEL_ENABLE_PROTOCOLS"] = "1"
print("🔧 Babbel CLI Test")
resp = process_message("I feel anxious and want one step.")
print(json.dumps(resp, indent=2))
