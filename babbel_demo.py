from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea
from PyQt6.QtCore import Qt
from babbel.engine import BabbelEngine
from babbel_gui.widgets.chat_bubble import ChatBubble

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Babbel Demo")
        self.engine = BabbelEngine()

        self.layout = QVBoxLayout(self)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        input_layout = QHBoxLayout()
        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.on_send)  # ✅ hit Enter to send
        self.send = QPushButton("Send", self)
        self.send.clicked.connect(self.on_send)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send)
        self.layout.addLayout(input_layout)

    def on_send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.add_bubble(text, "user")

        reply = self.engine.reply(text)
        self.add_bubble(reply["text"], "assistant", reply.get("emotions"), reply.get("meta"))

        self.input.clear()

    def add_bubble(self, text, role, emotions=None, meta=None):
        bubble = ChatBubble(text, role, emotions, show_metadata=True, meta=meta)
        self.scroll_layout.addWidget(bubble)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())
