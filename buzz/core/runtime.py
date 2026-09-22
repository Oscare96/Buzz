"""End-to-end Buzz request execution runtime."""

from __future__ import annotations

from dataclasses import dataclass
import json
from uuid import uuid4

from buzz.ai.provider import AIProvider
from buzz.core.planner import parse_plan, PlanError
from buzz.core.request import BuzzRequest, BuzzResponse
from buzz.core.router import ToolRouter
from buzz.security.approvals import ApprovalStore
from buzz.security.audit import AuditEvent
from buzz.memory.store import MemoryStore
from buzz.memory.context import ConversationContext


SYSTEM_INSTRUCTION = """You are Buzz's planning brain. Return JSON only with keys reply and actions.
Each action contains skill, arguments, and reason fields.
Never invent a skill. Available skills: {skills}.
If no tool is required, actions must be an empty array.
Buzz executes requested capabilities itself; do not tell the user to perform a supported action manually.
Sensitive actions remain subject to Buzz's independent authorization layer."""


@dataclass
class BuzzRuntime:
    provider: AIProvider
    router: ToolRouter
    approvals: ApprovalStore | None = None
    memory: MemoryStore | None = None

    def __post_init__(self) -> None:
        if self.approvals is None:
            self.approvals = ApprovalStore()

    def handle(self, request: BuzzRequest, *, confirmed: bool = False) -> BuzzResponse:
        skills = json.dumps(self.router.registry.planner_specs(), separators=(",", ":"))
        context = ConversationContext(self.memory).recent() if self.memory else []
        context_text = ("\nRecent context: " + json.dumps(context,ensure_ascii=False)) if context else ""
        prompt = SYSTEM_INSTRUCTION.format(skills=skills) + context_text + "\nUser request: " + request.text
        try:
            plan = parse_plan(self.provider.respond(prompt).text)
        except PlanError as exc:
            if self.router.audit_log is not None:
                self.router.audit_log.write(AuditEvent("ai.plan","rejected",f"request_id={request.request_id}; {exc}"))
            return BuzzResponse("I couldn't safely interpret that plan. Please try the request again.",request.request_id,{"actions":[],"pending_confirmation":[],"plan_error":True})
        results, pending = [], []\n        seen_actions: set[tuple[str,str]] = set()
        for action in plan.actions:
            arguments = dict(action.arguments)\n            fingerprint=(action.skill,json.dumps(arguments,sort_keys=True,separators=(",",":"),default=str))\n            if fingerprint in seen_actions:\n                results.append({"skill":action.skill,"arguments":arguments,"success":False,"message":"Duplicate action skipped."})\n                continue\n            seen_actions.add(fingerprint)
            if action.skill == "trading.place_order" and not arguments.get("idempotency_key"):
                arguments["idempotency_key"] = uuid4().hex
            result = self.router.execute(action.skill, confirmed=confirmed, **arguments)
            item = {"skill": action.skill, "arguments": arguments, "success": result.success, "message": result.message}
            results.append(item)
            if not result.success and "Confirmation required" in result.message:
                approval = self.approvals.issue(action.skill, arguments)
                if self.router.audit_log is not None:
                    self.router.audit_log.write(AuditEvent(action.skill,"approval_issued",f"request_id={request.request_id}; approval_token_issued"))
                pending.append({"skill": action.skill, "arguments": arguments, "reason": action.reason, "approval_token": approval.token})
        response = BuzzResponse(plan.reply, request.request_id, {"actions": results, "pending_confirmation": pending})
        if self.memory is not None:
            ConversationContext(self.memory).remember(request.text,plan.reply)
        return response

    def confirm(self, skill: str, arguments: dict, approval_token: str):
        if self.approvals is None or not self.approvals.consume(approval_token, skill, arguments):
            from buzz.skills.base import SkillResult
            if self.router.audit_log is not None:
                self.router.audit_log.write(AuditEvent(skill,"approval_rejected","Invalid, expired, reused, or mismatched approval."))
            return SkillResult(False, "Approval is invalid, expired, already used, or does not match this action.")
        return self.router.execute(skill, confirmed=True, **arguments)
