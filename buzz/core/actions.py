"""Structured action plans produced by Buzz reasoning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlannedAction:
    skill: str
    arguments: dict[str, Any] = field(default_factory=dict)
    reason: str = ""


@dataclass(frozen=True)
class ActionPlan:
    reply: str = ""
    actions: tuple[PlannedAction, ...] = ()
