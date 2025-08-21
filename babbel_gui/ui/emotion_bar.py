from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

class EmotionBar(QWidget):
    def __init__(self, values):
        super().__init__()
        self.setObjectName("EmotionBar")
        row = QHBoxLayout(self); row.setContentsMargins(0,6,0,0); row.setSpacing(3)
        values = list(values or [])
        if not values: values = [0.2]*16
        for v in values:
            seg = QFrame(); seg.setObjectName("EmotionSeg")
            h = max(6, int(26*float(v)))
            seg.setFixedSize(8, h)
            row.addWidget(seg, alignment=Qt.AlignmentFlag.AlignBottom)
