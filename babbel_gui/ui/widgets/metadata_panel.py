from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
import json

class MetadataPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._meta = {}
        lay = QVBoxLayout(self); lay.setContentsMargins(8,8,8,8); lay.setSpacing(6)
        self.lbl_title = QLabel("Metadata")
        self.lbl_emotion = QLabel("Emotion: —")
        self.lbl_tone = QLabel("Tone: —")
        self.lbl_intent = QLabel("Intent: —")
        self.lbl_node = QLabel("Node: —")
        self.lbl_safety = QLabel("Safety: —")
        self.lbl_tokens = QLabel("Tokens: —")
        self.lbl_summary = QLabel("Session: —")
        self.btn_raw = QPushButton("Raw JSON")
        self.raw = QTextEdit(); self.raw.setReadOnly(True); self.raw.hide()
        for w in (self.lbl_title,self.lbl_emotion,self.lbl_tone,self.lbl_intent,self.lbl_node,self.lbl_safety,self.lbl_tokens,self.lbl_summary,self.btn_raw,self.raw):
            lay.addWidget(w)
        self.btn_raw.clicked.connect(self._toggle_raw)

    def _toggle_raw(self):
        self.raw.setVisible(not self.raw.isVisible())

    def set_data(self, result: dict, session_stats: dict):
        meta = result.get("metadata") or {}
        self._meta = meta
        self.lbl_emotion.setText(f"Emotion: {meta.get('emotion','—')}")
        self.lbl_tone.setText(f"Tone: {meta.get('tone','—')}")
        self.lbl_intent.setText(f"Intent: {meta.get('intent','—')}")
        self.lbl_node.setText(f"Node: {meta.get('node','—')}")
        self.lbl_safety.setText(f"Safety: {', '.join(meta.get('safety_flags',[])) if meta.get('safety_flags') else '—'}")
        tok = meta.get('token_usage') or {}
        if tok:
            self.lbl_tokens.setText(f"Tokens: prompt {tok.get('prompt',0)}, completion {tok.get('completion',0)}, total {tok.get('total',0)}")
        else:
            self.lbl_tokens.setText("Tokens: —")
        self.lbl_summary.setText(f"Session: users {session_stats.get('user',0)}, assistant {session_stats.get('assistant',0)}, avg emotion {session_stats.get('avg_emotion','—')}")
        self.raw.setPlainText(json.dumps(result, indent=2))
