# main.py — Babbel GUI v6 (Full Integration: Waves 1–6)
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel,
    QScrollArea, QFrame, QHBoxLayout, QCheckBox, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QClipboard
import sys, os, json
from babbel_core.core.orchestrator import process_message
from babbel_core.core.config import load as load_config

class BabbelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Babbel")
        self.resize(800, 1000)
        self.setStyleSheet("background-color: #f7f7f8; font-family: -apple-system, sans-serif;")
        self.emotion_history = []
        self.memory_path = load_config().MEMORY_FILE

        self.layout = QVBoxLayout(self)
        self.setup_controls()
        self.setup_chat_area()
        self.setup_input_area()
        self.load_memory()

    def setup_controls(self):
        self.controls = QHBoxLayout()
        self.metadata_toggle = QCheckBox("Show Metadata")
        self.metadata_toggle.setChecked(True)
        self.auto_copy = QCheckBox("Auto-copy replies")

        self.culture_dropdown = QComboBox()
        self.culture_dropdown.addItems([
            "Disabled", "Japanese (jp)", "German (de)", "Arabic (ar)",
            "Chinese (zh)", "Spanish (es)", "French (fr)", "English (en)"
        ])

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_last)
        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self.export_memory)

        for w in [self.protocol_toggle, self.metadata_toggle, self.auto_copy,
                  QLabel("Culture:"), self.culture_dropdown,
                  self.undo_button, self.export_button]:
            self.controls.addWidget(w)
        self.layout.addLayout(self.controls)

    def setup_chat_area(self):
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.scroll.setWidget(self.chat_container)
        self.layout.addWidget(self.scroll)

    def setup_input_area(self):
        self.user_input = QTextEdit(self)
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.setFixedHeight(80)
        self.layout.addWidget(self.user_input)
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

    def set_env(self):
        os.environ["BABBEL_ENABLE_PROTOCOLS"] = "1" if self.protocol_toggle.isChecked() else "0"
        lang = self.culture_dropdown.currentText()
        if lang.lower().startswith("disabled"):
            os.environ.pop("BABBEL_CULTURE_SHIFT", None)
            os.environ.pop("BABBEL_TARGET_CULTURE", None)
        else:
            os.environ["BABBEL_CULTURE_SHIFT"] = "1"
            os.environ["BABBEL_TARGET_CULTURE"] = lang.split("(")[-1].strip(")")

    def send_message(self):
        text = self.user_input.toPlainText().strip()
        if not text:
            return
        self.user_input.clear()
        self.set_env()
        self.add_bubble(text, "user")
        response = process_message(text)
        self.add_bubble(response.get("final_text", "[No response]"), "babbel")
        self.add_annotation_panel(response)
        self.emotion_history.append(response.get("emotion", ""))
        if self.auto_copy.isChecked():
            QApplication.clipboard().setText(response.get("final_text", ""))

    def add_bubble(self, text, sender):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble.setStyleSheet(f"""
            QLabel {{
                background-color: {"#daf0ff" if sender=="user" else "#ffffff"};
                border-radius: 18px;
                padding: 12px;
                margin: 6px;
                font-size: 15px;
            }}
        """)
        self.chat_layout.addWidget(bubble)

    def add_annotation_panel(self, response):
        if not self.metadata_toggle.isChecked():
            return
        ux = response.get("ux", {})
        panel = QLabel()
        panel.setWordWrap(True)
        panel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        panel.setTextFormat(Qt.TextFormat.RichText)
        emotion = response.get("emotion", "").capitalize()
        intent = response.get("intent", "").capitalize()
        reflection = ux.get("reflection", "")
        question = ux.get("question", "")
        cta = ux.get("cta", "")
        explanation = ux.get("culture_explanation", "")
        choices = ux.get("choices", [])

        text = f"""
<b>😔 Emotion:</b> {emotion}   <b>🌟 Intent:</b> {intent}
<b>✨ Reflection:</b> {reflection}
<b>🛍 Options:</b>
"""
        for c in choices:
            text += f"• <b>{c.get('label')}</b>: {c.get('first_step')}\n"
        if question:
            text += f"<b>❓ {question}</b>\n"
        if cta:
            text += f"<b>➡️ {cta}</b>\n"
        if explanation:
            text += f"<em>{explanation}</em>"

        panel.setText(text)
        panel.setStyleSheet("""
            QLabel {
                background-color: #eef1f4;
                border-left: 4px solid #00acc1;
                padding: 10px;
                margin: 4px 6px 14px 6px;
                font-size: 13px;
            }
        """)
        self.chat_layout.addWidget(panel)

    def undo_last(self):
        count = self.chat_layout.count()
        if count >= 2:
            for _ in range(2):
                item = self.chat_layout.itemAt(count - 1)
                widget = item.widget()
                self.chat_layout.removeWidget(widget)
                widget.setParent(None)
                count -= 1
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data = data[:-1]
                with open(self.memory_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    def load_memory(self):
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    data = json.load(f)[-5:]
                for entry in data:
                    self.add_bubble(entry.get("user_input", ""), "user")
                    self.add_bubble(entry.get("response", ""), "babbel")
            except Exception:
                pass

    def export_memory(self):
        os.system("python3 babbel_core/scripts/export_history_csv.py")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BabbelApp()
    window.show()
    sys.exit(app.exec())
