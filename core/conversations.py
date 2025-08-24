import os
def list_sessions(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    return sorted(files, key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
