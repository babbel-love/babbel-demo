from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel, QVBoxLayout, QScrollArea

class MetadataPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MetadataPanel")
        v = QVBoxLayout(self)
        title = QLabel("Metadata"); title.setObjectName("MetaTitle")
        self.form = QFormLayout()
        wrap = QWidget(); wrap.setLayout(self.form)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(wrap)
        v.addWidget(title); v.addWidget(scroll)
        self.labels = {}

    def update(self, meta: dict):
        for k, v in (meta or {}).items():
            if isinstance(v, (dict, list)): v = str(v)
            if k not in self.labels:
                lab = QLabel(str(v)); lab.setWordWrap(True)
                self.form.addRow(QLabel(k.capitalize()+":"), lab); self.labels[k]=lab
            else:
                self.labels[k].setText(str(v))
