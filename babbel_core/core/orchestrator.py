from core.pipeline import run_pipeline

class Orchestrator:
    def __init__(self):
        pass

    def send_thread(self, thread_dict):
        user_input = thread_dict["messages"][-1]["content"]
        final = run_pipeline(user_input)
        return {"text": final}
