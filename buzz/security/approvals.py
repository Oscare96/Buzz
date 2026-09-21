"""Short-lived approval tokens for sensitive Buzz actions."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from uuid import uuid4


@dataclass(frozen=True)
class Approval:
    token: str
    skill: str
    expires_at: float


class ApprovalStore:
    def __init__(self) -> None:
        self._items: dict[str, Approval] = {}

    def issue(self, skill: str, ttl_seconds: float = 60.0) -> Approval:
        approval = Approval(uuid4().hex, skill, monotonic() + ttl_seconds)
        self._items[approval.token] = approval
        return approval

    def consume(self, token: str, skill: str) -> bool:
        approval = self._items.pop(token, None)
        return bool(approval and approval.skill == skill and monotonic() <= approval.expires_at)
