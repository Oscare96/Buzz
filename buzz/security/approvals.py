"""Short-lived, single-use approval tokens for sensitive Buzz actions."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from time import monotonic
from typing import Any
from uuid import uuid4


def action_fingerprint(skill: str, arguments: dict[str, Any]) -> str:
    payload = json.dumps({"skill": skill, "arguments": arguments}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Approval:
    token: str
    fingerprint: str
    expires_at: float


class ApprovalStore:
    def __init__(self) -> None:
        self._items: dict[str, Approval] = {}

    def issue(self, skill: str, arguments: dict[str, Any], ttl_seconds: float = 60.0) -> Approval:
        approval = Approval(uuid4().hex, action_fingerprint(skill, arguments), monotonic() + ttl_seconds)
        self._items[approval.token] = approval
        return approval

    def consume(self, token: str, skill: str, arguments: dict[str, Any]) -> bool:
        approval = self._items.pop(token, None)
        return bool(approval and approval.fingerprint == action_fingerprint(skill, arguments) and monotonic() <= approval.expires_at)
