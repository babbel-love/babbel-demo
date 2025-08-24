class MemoryStore:
    def __init__(self):
        self.sessions = {}
        self.current_session = None

    def start_new_session(self):
        self.current_session = {"messages": [], "meta": {}}

    def add_message(self, role, content):
        if self.current_session is None:
            self.start_new_session()
        self.current_session["messages"].append({"role": role, "content": content})

    def get_session(self):
        return self.current_session or {"messages": []}
