"""End-to-end Buzz request execution runtime."""

from __future__ import annotations

from dataclasses import dataclass
import json

from buzz.ai.provider import AIProvider
from buzz.core.planner import parse_plan
from buzz.core.request import BuzzRequest, BuzzResponse
from buzz.core.router import ToolRouter
from buzz.security.approvals import ApprovalStore
from buzz.memory.store import MemoryStore


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
        context = self.memory.get("conversation","last_exchange") if self.memory else None
        context_text = ("\nRecent context: " + json.dumps(context,ensure_ascii=False)) if context else ""
        prompt = SYSTEM_INSTRUCTION.format(skills=skills) + context_text + "\nUser request: " + request.text
        plan = parse_plan(self.provider.respond(prompt).text)
        results, pending = [], []
        for action in plan.actions:
            result = self.router.execute(action.skill, confirmed=confirmed, **action.arguments)
            item = {"skill": action.skill, "arguments": action.arguments, "success": result.success, "message": result.message}
            results.append(item)
            if not result.success and "Confirmation required" in result.message:
                approval = self.approvals.issue(action.skill, action.arguments)
                pending.append({"skill": action.skill, "arguments": action.arguments, "reason": action.reason, "approval_token": approval.token})
        response = BuzzResponse(plan.reply, request.request_id, {"actions": results, "pending_confirmation": pending})
        if self.memory is not None:
            self.memory.put("conversation","last_exchange",{"user":request.text,"assistant":plan.reply})
        return response

    def confirm(self, skill: str, arguments: dict, approval_token: str):
        if self.approvals is None or not self.approvals.consume(approval_token, skill, arguments):
            from buzz.skills.base import SkillResult
            return SkillResult(False, "Approval is invalid, expired, already used, or does not match this action.")
        return self.router.execute(skill, confirmed=True, **arguments)
