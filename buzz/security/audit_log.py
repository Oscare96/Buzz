"""Append-only JSON-lines audit log for local Buzz actions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from buzz.security.audit import AuditEvent


_SECRET_PATTERNS=(
    re.compile(r"(?i)(authorization|api[_ -]?key|secret[_ -]?key|access[_ -]?token)\\s*[=:]\\s*[^;\\s,]+"),
    re.compile(r"(?i)bearer\\s+[A-Za-z0-9._-]+"),
)

def _redact(value: str) -> str:
    for pattern in _SECRET_PATTERNS:
        value=pattern.sub("[REDACTED]",value)
    return value

class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            payload=event.as_dict()
            payload["detail"]=_redact(str(payload.get("detail","")))
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

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
