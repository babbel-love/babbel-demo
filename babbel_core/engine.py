from __future__ import annotations
from types import SimpleNamespace
from typing import Tuple
from .thread import ConversationThread
from .emotion_classifier import classify_emotion
from .intent_classifier import classify_intent
from .node_rewrite_v2 import run_node_rewrite
from .review import run_review_stage
from .chat import use_chat

class BabbelEngine:
    def __init__(self, apply_style: bool = True):
        self.apply_style = apply_style

    def turn(self, thread: ConversationThread, user_text: str) -> Tuple[str,str,str,ConversationThread]:
        thread.add_message("user", user_text)
        result = use_chat(thread.to_dict())  # {"messages":[SimpleNamespace(role, content)]}
        try:
            assistant_text = result["messages"][0].content
        except Exception:
            assistant_text = "OK."
        emo = classify_emotion(user_text)
        intent = classify_intent(user_text)
        final = run_review_stage(run_node_rewrite(assistant_text, emo, intent))
        thread.add_message("assistant", final)
        return final, emo, intent, thread
