"""End-to-end Buzz request execution runtime."""

from __future__ import annotations

from dataclasses import dataclass
import json

from buzz.ai.provider import AIProvider
from buzz.core.planner import parse_plan
from buzz.core.request import BuzzRequest, BuzzResponse
from buzz.core.router import ToolRouter


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

    def handle(self, request: BuzzRequest, *, confirmed: bool = False) -> BuzzResponse:
        skills = json.dumps(self.router.registry.planner_specs(), separators=(",", ":"))
        prompt = SYSTEM_INSTRUCTION.format(skills=skills) + "\nUser request: " + request.text
        plan = parse_plan(self.provider.respond(prompt).text)
        results, pending = [], []
        for action in plan.actions:
            result = self.router.execute(action.skill, confirmed=confirmed, **action.arguments)
            item = {"skill": action.skill, "arguments": action.arguments, "success": result.success, "message": result.message}
            results.append(item)
            if not result.success and "Confirmation required" in result.message:
                pending.append({"skill": action.skill, "arguments": action.arguments, "reason": action.reason})
        return BuzzResponse(plan.reply, request.request_id, {"actions": results, "pending_confirmation": pending})
