from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from .emotion_bar import EmotionBar

class MessageBubble(QWidget):
    def __init__(self, text: str, role: str="user", meta=None, ebar=None):
        super().__init__()
        self.setObjectName("MsgBubble_"+role)
        lay = QVBoxLayout(self)
        lab = QLabel(text); lab.setWordWrap(True)
        lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lay.addWidget(lab)
        if role == "assistant":
            if ebar: lay.addWidget(EmotionBar(ebar))
            if meta:
                cap = QLabel(f"{meta.get('emotion','neutral')} · {meta.get('tone','balanced')} · {meta.get('intent','inform')} · {meta.get('node','')}")
                cap.setObjectName("MetaCaption"); lay.addWidget(cap)
        op = QGraphicsOpacityEffect(self); self.setGraphicsEffect(op)
        anim = QPropertyAnimation(op, b"opacity", self)
        anim.setDuration(260); anim.setStartValue(0.0); anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad); anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
