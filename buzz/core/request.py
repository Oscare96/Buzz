"""Structured requests and responses flowing through Buzz."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class BuzzRequest:
    text: str
    source: str = "text"
    request_id: str = field(default_factory=lambda: uuid4().hex)


@dataclass(frozen=True)
class BuzzResponse:
    text: str
    request_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
