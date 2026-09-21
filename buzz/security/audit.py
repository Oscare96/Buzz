"""Structured audit records for actions Buzz attempts."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    action: str
    outcome: str
    detail: str = ""
    timestamp: str = ""

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["timestamp"] = self.timestamp or datetime.now(timezone.utc).isoformat()
        return payload
