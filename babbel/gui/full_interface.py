from babbel.gui.interface_memory import BabbelGUIInterface
from babbel.gui.interface_retry import BabbelGUIRetry

class BabbelFullGUI(BabbelGUIInterface, BabbelGUIRetry):
    def __init__(self):
        BabbelGUIInterface.__init__(self)
        BabbelGUIRetry.__init__(self)
    def send_input(self, text: str):
        reply_retry = BabbelGUIRetry.send_user_input(self, text)
        reply_memory = BabbelGUIInterface.send_user_input(self, text)
        return {"retry": reply_retry, "memory": reply_memory}
    def last_emotion(self):
        return self.get_last_emotion()
    def last_node(self):
        return self.get_last_node()
