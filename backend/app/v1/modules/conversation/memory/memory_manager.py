class MemoryManager:
    def __init__(self):
        self.sessions = {}  # { user_id: [messages...] }

    def get_history(self, user_id: str):
        return self.sessions.get(user_id, [])

    def add_message(self, user_id: str, role: str, content: str):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append({"role": role, "content": content})
