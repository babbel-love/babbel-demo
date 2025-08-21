from __future__ import annotations
from typing import Dict, Optional
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QFontMetrics, QPaintEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout

DEFAULT_EMOTIONS = ["joy", "sadness", "anger", "fear", "disgust", "surprise", "neutral"]

class MiniEmotionBar(QWidget):
    """Tiny horizontal strip showing per-emotion proportions as segments."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scores: Dict[str, float] = {}
        self.setMinimumHeight(6)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip("Per-message emotion proportions")

    def set_scores(self, scores: Dict[str, float]) -> None:
        self._scores = scores or {}
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(120, 6)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Normalize scores
        keys = list(self._scores.keys()) or DEFAULT_EMOTIONS
        total = sum(max(0.0, float(self._scores.get(k, 0.0))) for k in keys)
        if total <= 0:
            painter.fillRect(0, 0, w, h, self.palette().mid())
            return

        # Draw contiguous segments without choosing specific colors (use palette variations)
        x = 0.0
        for i, k in enumerate(keys):
            frac = max(0.0, float(self._scores.get(k, 0.0))) / total
            seg_w = frac * w
            # Alternate between highlight/mid to avoid hard-coded colors
            brush = self.palette().highlight() if (i % 2 == 0) else self.palette().mid()
            painter.fillRect(int(x), 0, int(seg_w), h, brush)
            x += seg_w

class BubbleFrame(QFrame):
    """Rounded frame that looks like a chat bubble."""
    def __init__(self, role: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.setObjectName("bubble")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setProperty("role", role)
        self.setStyleSheet("""
            QFrame#bubble[role="user"] {
                background-color: #2e2f31;
                color: #ffffff;
                border-radius: 18px;
                padding: 10px 12px;
            }
            QFrame#bubble[role="assistant"] {
                background-color: #1f1f20;
                color: #eaeaea;
                border-radius: 18px;
                padding: 10px 12px;
            }
        """)

class MessageBubble(QWidget):
    """
    Composite widget: rounded bubble + text + (optional) mini emotion bar.
    role: "user" | "assistant"
    """
    def __init__(self, role: str, text: str, emotions: Optional[Dict[str, float]] = None, show_metadata: bool = True, parent=None):
        super().__init__(parent)
        self.role = role
        self._show_metadata = show_metadata

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 6, 12, 6)

        self.bubble = BubbleFrame(role, self)
        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(12, 8, 12, 8)

        self.lbl = QLabel(text, self.bubble)
        self.lbl.setWordWrap(True)
        self.lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble_layout.addWidget(self.lbl)

        row = QHBoxLayout()
        row.setContentsMargins(0,0,0,0)
        row.setSpacing(8)
        bubble_layout.addLayout(row)

        self.emobadge = QLabel("", self.bubble)
        self.emobadge.setObjectName("emobadge")
        self.emobadge.setStyleSheet("QLabel#emobadge { border-radius: 10px; padding: 2px 8px; background: #2a2a2b; color: #cccccc; font-size: 11px; }")
        row.addWidget(self.emobadge, 0, Qt.AlignmentFlag.AlignLeft)

        row.addStretch(1)

        self.emobar = MiniEmotionBar(self.bubble)
        bubble_layout.addWidget(self.emobar)
        self.emobar.setVisible(bool(show_metadata and emotions))
        if emotions:
            self.emobar.set_scores(emotions)

        self._apply_emobadge(emotions if show_metadata else None)

        # alignment: user on right, assistant on left
        if role == "user":
            outer.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.bubble.setMaximumWidth(820)
        else:
            outer.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.bubble.setMaximumWidth(820)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

    def set_emotions(self, emotions: Optional[Dict[str, float]]) -> None:
        self.emobar.setVisible(bool(self._show_metadata and emotions))
        if emotions:
            self.emobar.set_scores(emotions)
        self._apply_emobadge(emotions)

    def set_show_metadata(self, on: bool) -> None:
        self._show_metadata = on
        self.emobar.setVisible(on and self.emobar.isVisible())
        self._apply_emobadge(None if not on else self.emobar._scores if hasattr(self.emobar,'_scores') else None)

    def minimumSizeHint(self) -> QSize:
        fm = QFontMetrics(self.font())
        h = fm.lineSpacing() * 2 + 24
        return QSize(120, h)


    def _top1(self, emotions):
        try:
            items = list((k, float(v)) for k,v in emotions.items())
            if not items: return None
            items.sort(key=lambda kv: kv[1], reverse=True)
            return items[0]
        except Exception:
            return None

    def _apply_emobadge(self, emotions):
        if self._show_metadata and emotions:
            top = self._top1(emotions)
            if top:
                k, v = top
                self.emobadge.setText(f"{k} · {v:.2f}")
                self.emobadge.show()
                return
        self.emobadge.hide()
