"""Persistent non-secret Buzz memory stored locally as JSON."""
from __future__ import annotations
import json
from pathlib import Path
from threading import RLock
from typing import Any
from buzz.memory.store import MemoryStore

class JsonMemoryStore(MemoryStore):
    def __init__(self,path:Path=Path(".cache/buzz/memory.json"))->None:
        self.path=path; self._lock=RLock()
    def _load(self)->dict[str,Any]:
        if not self.path.exists(): return {}
        try:
            value=json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value,dict) else {}
        except OSError:
            return {}
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Buzz memory file is corrupted: {self.path}. Refusing to overwrite it.") from exc
    def put(self,namespace:str,key:str,value:Any)->None:
        with self._lock:
            data=self._load(); data.setdefault(namespace,{})[key]=value
            self.path.parent.mkdir(parents=True,exist_ok=True)
            temp=self.path.with_suffix(".tmp"); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); temp.replace(self.path)
    def get(self,namespace:str,key:str)->Any|None:
        with self._lock: return self._load().get(namespace,{}).get(key)
