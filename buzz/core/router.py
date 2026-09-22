"""Route approved tool calls to registered Buzz skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from buzz.core.execution import ExecutionRecord

from buzz.core.verification import verify_success
from buzz.core.arguments import validate_arguments
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
        record=ExecutionRecord(skill=skill_name,arguments=dict(kwargs))
        execution_id=record.execution_id
        skill = self.registry.get(skill_name)
        validation_error = validate_arguments(skill.argument_schema, kwargs)
        if validation_error:
            result = SkillResult(False, validation_error, {"execution_id": execution_id})
            self._audit(skill_name, "blocked", execution_id, validation_error)
            return result
        decision = authorize(skill.risk_level, confirmed=confirmed)
        if not decision.allowed:
            result = SkillResult(False, decision.reason, {"execution_id": execution_id})
            self._audit(skill_name, "blocked", execution_id, decision.reason)
            return result
        try:
            record.attempted=True
            result = skill.execute(**kwargs)
        except Exception as exc:
            result = SkillResult(False, f"Execution failed: {exc}")
        record.success=result.success
        record.message=result.message
        record.data=result.data
        verification = verify_success(result)
        outcome = "verified" if verification.verified else "failed"
        self._audit(skill_name, outcome, execution_id, result.message)
        data = {"execution_id": execution_id, "result": result.data, "verified": verification.verified}
        return SkillResult(result.success, result.message, data)

    def _audit(self, action: str, outcome: str, execution_id: str, detail: str) -> None:
        if self.audit_log is not None:
            self.audit_log.write(AuditEvent(action, outcome, f"execution_id={execution_id}; {detail}"))
