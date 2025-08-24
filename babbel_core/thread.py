import uuid, json

class ConversationThread:
    def __init__(self, name, model="openrouter/auto", temperature=0.5, max_tokens=800):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def to_dict(self):
        return {
            "name": self.name,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": self.messages
        }

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

class SessionStore:
    def __init__(self):
        self.threads = {}

    def add_thread(self, thread):
        self.threads[thread.name] = thread

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in self.threads.items()}, f, indent=2)
