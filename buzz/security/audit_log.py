"""Append-only JSON-lines audit log for local Buzz actions."""

from __future__ import annotations

import json
from pathlib import Path

from buzz.security.audit import AuditEvent


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.as_dict(), ensure_ascii=False) + "\n")

    def read_recent(self, limit: int = 50) -> list[dict]:
        if limit <= 0 or not self.path.exists():
            return []
        lines=self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        events=[]
        for line in lines:
            try:
                value=json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value,dict):
                events.append(value)
        return events
