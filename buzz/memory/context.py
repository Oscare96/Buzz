"""Conversation context policy for Buzz local memory."""
from __future__ import annotations
import re
from typing import Any
from buzz.memory.store import MemoryStore

_SENSITIVE=re.compile(r"(?i)\b(password|passwd|api[_ -]?key|secret[_ -]?key|access[_ -]?token|bearer\s+[A-Za-z0-9._-]+)\b")
_LONG_TOKEN=re.compile(r"\b[A-Za-z0-9_-]{40,}\b")

def is_sensitive_text(text:str)->bool:
    return bool(_SENSITIVE.search(text) or _LONG_TOKEN.search(text))

class ConversationContext:
    def __init__(self,store:MemoryStore,max_exchanges:int=6)->None:
        self.store=store; self.max_exchanges=max(1,max_exchanges)
    def recent(self)->list[dict[str,str]]:
        value=self.store.get("conversation","recent")
        if not isinstance(value,list): return []
        clean=[]
        for item in value[-self.max_exchanges:]:
            if isinstance(item,dict) and isinstance(item.get("user"),str) and isinstance(item.get("assistant"),str):
                user=item["user"][:4000]; assistant=item["assistant"][:8000]
                if not is_sensitive_text(user) and not is_sensitive_text(assistant):
                    clean.append({"user":user,"assistant":assistant})
        return clean
    def remember(self,user:str,assistant:str)->bool:
        user=user[:4000]; assistant=assistant[:8000]
        if is_sensitive_text(user) or is_sensitive_text(assistant):
            return False
        history=self.recent(); history.append({"user":user,"assistant":assistant})
        self.store.put("conversation","recent",history[-self.max_exchanges:])
        return True
