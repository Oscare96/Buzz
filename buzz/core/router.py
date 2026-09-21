"""Route approved tool calls to registered Buzz skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from buzz.security.policy import authorize
from buzz.skills.base import SkillResult
from buzz.skills.registry import SkillRegistry


@dataclass
class ToolRouter:
    registry: SkillRegistry

    def execute(self, skill_name: str, *, confirmed: bool = False, **kwargs: Any) -> SkillResult:
        skill = self.registry.get(skill_name)
        decision = authorize(skill.risk_level, confirmed=confirmed)
        if not decision.allowed:
            return SkillResult(False, decision.reason)
        return skill.execute(**kwargs)
