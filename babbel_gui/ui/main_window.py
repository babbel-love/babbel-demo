from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar, QFileDialog, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt
from babbel_gui.adapters.bridge import get_babbel_response
from babbel_gui.utils import config as cfg
from .sidebar import Sidebar
from .widgets.trend_strip import TrendStrip
from .widgets.settings_dialog import SettingsDialog
from .widgets.toast import Toast
from .widgets.message_bubble import MessageBubble
from .widgets.metadata_panel import MetadataPanel
import json, os, time
from collections import Counter

SESS_DIR = os.path.expanduser("~/Downloads/Babbel_Sessions")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        d = cfg.load().get("defaults", {})
        self._show_metadata = d.get("show_metadata", True)
        self._live_preview  = d.get("live_preview", True)
        self._extra_state = {
            "emotion_savvy": d.get("emotion_savvy", False),
            "emit_emotion_series": d.get("emit_emotion_series", False),
            "cultural_sensitivity": d.get("cultural_sensitivity", False) }

        m = QMenuBar(self); self.setMenuBar(m)
        s = m.addMenu("Babbel")
        s.addAction("Settings…", self._open_settings)
        s.addAction("Export JSON…", self._export_json)
        s.addAction("Save Session", self._quick_save_session)
        s.addAction("Load Session…", self._load_session_dialog)

        root = QWidget(self); rootLay = QHBoxLayout(root); rootLay.setContentsMargins(8,8,8,8); rootLay.setSpacing(8)

        self.sidebar = Sidebar(show_metadata=self._show_metadata, live_preview=self._live_preview)        self.sidebar.metadataToggled.connect(self._toggle_meta)
        self.sidebar.livePreviewToggled.connect(lambda v: setattr(self,"_live_preview",v))
        self.sidebar.extraTogglesChanged.connect(self._extra_state.update)
        self.sidebar.sessionChosen.connect(self._load_session)
        rootLay.addWidget(self.sidebar, 1)

        center = QWidget(root); centerLay = QVBoxLayout(center); centerLay.setContentsMargins(8,8,8,8); centerLay.setSpacing(8)
        self._typing = QLabel("…typing"); self._typing.setStyleSheet("color:#888;font-style:italic;"); self._typing.hide(); centerLay.addWidget(self._typing)
        self._trend = TrendStrip(center); self._trend.hide(); centerLay.addWidget(self._trend)
        self._toast = Toast(center); centerLay.addWidget(self._toast)
        self._scroll = QScrollArea(center); self._scroll.setWidgetResizable(True); centerLay.addWidget(self._scroll, 1)
        self._feed = QWidget(self._scroll); self._feedLay = QVBoxLayout(self._feed); self._feedLay.addStretch(1); self._scroll.setWidget(self._feed)
        self._meta_panel = MetadataPanel(center); self._meta_panel.setVisible(self._show_metadata); centerLay.addWidget(self._meta_panel)
        rootLay.addWidget(center, 3)

        self.setCentralWidget(root)
        self._messages=[]

        try:
            self.sidebar.refreshSessions()
        except Exception:
            pass

    def _clear_feed(self):
        while self._feedLay.count() > 1:
            item = self._feedLay.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()

    def add_user(self, text):
        b = MessageBubble(text, role="user", ts=time.time()); self._feedLay.insertWidget(self._feedLay.count()-1, b)
        self._messages.append({"role":"user","text":text,"ts":time.time()})

    def add_bot(self, text, meta):
        b = MessageBubble(text, role="assistant", ts=time.time()); self._feedLay.insertWidget(self._feedLay.count()-1, b)
        self._scroll.verticalScrollBar().setValue(self._scroll.verticalScrollBar().maximum())
        self._messages.append({"role":"assistant","meta":meta,"text":text,"ts":time.time()})

    def _sendMessage(self, text):
        if not text.strip(): return
        self.add_user(text); self._typing.show()
        try:
            result = get_babbel_response(text,
                show_metadata=self._show_metadata, live_preview=self._live_preview,
                **self._extra_state, session=None)
            self._typing.hide()
            self._renderAssistant(result)
        except Exception as e:
            self._typing.hide(); self._toast.show_msg(f"Error: {e}")

    def _renderAssistant(self, result):
        out_text = result.get("final_text") or result.get("reply_text") or ""
        meta = result.get("metadata") or {}
        self.add_bot(out_text, meta)
        if self._extra_state.get("emit_emotion_series") and result.get("session_emotions"):
            self._trend.set(result["session_emotions"]); self._trend.show()
        else:
            self._trend.hide()
        stats = self._session_stats()
        if self._show_metadata:
            self._meta_panel.set_data(result, stats)

    def _session_stats(self):
        users = sum(1 for m in self._messages if m["role"]=="user")
        bots  = sum(1 for m in self._messages if m["role"]=="assistant")
        emos = [ (m.get("meta") or {}).get("emotion") for m in self._messages if m["role"]=="assistant" and (m.get("meta") or {}).get("emotion")]
        avg = "—"
        if emos:
            from collections import Counter
            avg = Counter([e.lower() for e in emos]).most_common(1)[0][0]
        return {"user": users, "assistant": bots, "avg_emotion": avg}

    def _toggle_meta(self, state: bool):
        self._show_metadata = state
        self._meta_panel.setVisible(state)

    def _open_settings(self): SettingsDialog.edit(self); self._toast.show_msg("Settings saved")

    def _export_json(self):
        os.makedirs(SESS_DIR,exist_ok=True)
        path,_=QFileDialog.getSaveFileName(self,"Export JSON",os.path.join(SESS_DIR,"session.json"),"JSON (*.json)")
        if not path: return
        with open(path,"w") as f:
            json.dump({
                "toggles": { **self._extra_state, "show_metadata":self._show_metadata, "live_preview":self._live_preview},
                "messages":self._messages
            },f,indent=2)
        self._toast.show_msg("Exported JSON")
        try: self.sidebar.refreshSessions()
        except Exception: pass

    def _quick_save_session(self):
        os.makedirs(SESS_DIR,exist_ok=True)
        fn=os.path.join(SESS_DIR,f"babbel_{int(time.time())}.json")
        with open(fn,"w") as f: json.dump({"messages":self._messages},f,indent=2)
        self._toast.show_msg("Saved session")
        try: self.sidebar.refreshSessions()
        except Exception: pass

    def _load_session_dialog(self):
        os.makedirs(SESS_DIR,exist_ok=True)
        path,_=QFileDialog.getOpenFileName(self,"Load Session",SESS_DIR,"JSON (*.json)")
        if path: self._load_session(path)

    def _load_session(self, path: str):
        try:
            with open(path,"r") as f: data = json.load(f)
            msgs = data.get("messages") or []
            self._messages = []
            self._clear_feed()
            for m in msgs:
                if m.get("role")=="user":
                    self.add_user(m.get("text",""))
                elif m.get("role")=="assistant":
                    txt = m.get("text") or ((m.get("result") or {}).get("final_text") or (m.get("result") or {}).get("reply_text") or "")
                    meta = m.get("meta") or (m.get("result") or {}).get("metadata") or {}
                    self.add_bot(txt, meta)
            self._toast.show_msg("Session loaded")
        except Exception as e:
            self._toast.show_msg(f"Load failed: {e}")
