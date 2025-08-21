from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton

class BabbelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Babbel Patched")
        self.setMinimumSize(800, 600)

        self.textbox = QTextEdit()
        self.button = QPushButton("Send")
        self.metadata_panel = QLabel()
        self.output = QLabel()

        self.button.clicked.connect(self.fake_response)

        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        layout.addWidget(self.output)
        layout.addWidget(self.metadata_panel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def fake_response(self):
        user_input = self.textbox.toPlainText()
        # fake response format
        response = {
            "final_text": f"Echo: {user_input}",
            "intent_label": "Curiosity",
            "emotion_label": "Neutral",
            "tone": "Conversational",
            "culture_explanation": "No cultural shift needed."
        }
        self.render_response(response)

    def render_response(self, response):
        reply_text = response.get("final_text", "No response.")
        self.output.setText(reply_text)

        intent = response.get("intent_label", "Unknown")
        emotion = response.get("emotion_label", "Unknown")
        tone = response.get("tone", "Neutral")
        culture_note = response.get("culture_explanation", "")

        meta = f"<b>Intent:</b> {intent} &nbsp;&nbsp; <b>Emotion:</b> {emotion} &nbsp;&nbsp; <b>Tone:</b> {tone}"
        if culture_note:
            meta += f"<br><i>Cultural Note:</i> {culture_note}"

        self.metadata_panel.setText(meta)
        self.metadata_panel.show()

if __name__ == "__main__":
    app = QApplication([])
    window = BabbelApp()
    window.show()
    app.exec()
