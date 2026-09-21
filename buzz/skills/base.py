"""Contracts for trusted Buzz skills."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from buzz.security.risk import RiskLevel


@dataclass(frozen=True)
class SkillResult:
    success: bool
    message: str
    data: Any = None


class Skill(ABC):
    name: str
    description: str
    risk_level: RiskLevel = RiskLevel.READ
    argument_schema: dict[str, Any] = {"type": "object", "properties": {}, "additionalProperties": False}

    def planner_spec(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "arguments": self.argument_schema}

    @abstractmethod
    def execute(self, **kwargs: Any) -> SkillResult:
        raise NotImplementedError
