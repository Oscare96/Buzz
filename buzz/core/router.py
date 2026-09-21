"""Route approved tool calls to registered Buzz skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from buzz.security.audit import AuditEvent
from buzz.security.audit_log import AuditLog
from buzz.security.policy import authorize
from buzz.skills.base import SkillResult
from buzz.skills.registry import SkillRegistry


@dataclass
class ToolRouter:
    registry: SkillRegistry
    audit_log: AuditLog | None = None

    def execute(self, skill_name: str, *, confirmed: bool = False, **kwargs: Any) -> SkillResult:
        skill = self.registry.get(skill_name)
        decision = authorize(skill.risk_level, confirmed=confirmed)
        if not decision.allowed:
            result = SkillResult(False, decision.reason)
            self._audit(skill_name, "blocked", decision.reason)
            return result
        try:
            result = skill.execute(**kwargs)
        except Exception as exc:
            result = SkillResult(False, f"Execution failed: {exc}")
        self._audit(skill_name, "success" if result.success else "failed", result.message)
        return result

    def _audit(self, action: str, outcome: str, detail: str) -> None:
        if self.audit_log is not None:
            self.audit_log.write(AuditEvent(action, outcome, detail))
