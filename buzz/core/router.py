"""Route approved tool calls to registered Buzz skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from buzz.core.verification import verify_success
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
        execution_id = uuid4().hex
        skill = self.registry.get(skill_name)
        decision = authorize(skill.risk_level, confirmed=confirmed)
        if not decision.allowed:
            result = SkillResult(False, decision.reason, {"execution_id": execution_id})
            self._audit(skill_name, "blocked", execution_id, decision.reason)
            return result
        try:
            result = skill.execute(**kwargs)
        except Exception as exc:
            result = SkillResult(False, f"Execution failed: {exc}")
        verification = verify_success(result)
        outcome = "verified" if verification.verified else "failed"
        self._audit(skill_name, outcome, execution_id, result.message)
        data = {"execution_id": execution_id, "result": result.data, "verified": verification.verified}
        return SkillResult(result.success, result.message, data)

    def _audit(self, action: str, outcome: str, execution_id: str, detail: str) -> None:
        if self.audit_log is not None:
            self.audit_log.write(AuditEvent(action, outcome, f"execution_id={execution_id}; {detail}"))
