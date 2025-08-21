from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QCheckBox, QPushButton, QComboBox, QHBoxLayout
from babbel_gui.utils import config as cfg

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Babbel Settings")
        self.setMinimumWidth(360)
        self._cfg = cfg.load()
        d = self._cfg.get("defaults", {})

        lay = QVBoxLayout(self)

        self.api = QLineEdit(self._cfg.get("api_key","")); self.api.setPlaceholderText("API key (optional)")
        lay.addWidget(QLabel("API key")); lay.addWidget(self.api)

        self.profile = QComboBox(); self.profile.addItems(["warm_coach","neutral","succinct"])
        ix = max(0, self.profile.findText(self._cfg.get("model_profile","warm_coach")))
        self.profile.setCurrentIndex(ix)
        lay.addWidget(QLabel("Model/style profile")); lay.addWidget(self.profile)

        self.savvy = QCheckBox("Default: Emotion Savvy"); self.savvy.setChecked(d.get("emotion_savvy",False)); lay.addWidget(self.savvy)
        self.track = QCheckBox("Default: Emotion Tracker"); self.track.setChecked(d.get("emit_emotion_series",False)); lay.addWidget(self.track)
        self.cult  = QCheckBox("Default: Cultural Sensitivity"); self.cult.setChecked(d.get("cultural_sensitivity",False)); lay.addWidget(self.cult)
        self.meta  = QCheckBox("Default: Show Metadata"); self.meta.setChecked(d.get("show_metadata",True)); lay.addWidget(self.meta)
        self.prev  = QCheckBox("Default: Live Emotion Preview"); self.prev.setChecked(d.get("live_preview",True)); lay.addWidget(self.prev)

        row = QHBoxLayout(); save_btn = QPushButton("Save"); cancel_btn = QPushButton("Cancel")
        row.addWidget(save_btn); row.addWidget(cancel_btn); lay.addLayout(row)
        save_btn.clicked.connect(self._save); cancel_btn.clicked.connect(self.reject)

    def _save(self):
        self._cfg["api_key"] = self.api.text().strip()
        self._cfg["model_profile"] = self.profile.currentText()
        self._cfg["defaults"] = {
            "emotion_savvy": self.savvy.isChecked(),
            "emit_emotion_series": self.track.isChecked(),
            "cultural_sensitivity": self.cult.isChecked(),
            "show_metadata": self.meta.isChecked(),
            "live_preview": self.prev.isChecked(),
        }
        cfg.save(self._cfg); self.accept()

    @staticmethod
    def edit(parent=None):
        dlg = SettingsDialog(parent); return dlg.exec()
