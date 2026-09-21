"""End-to-end Buzz request execution runtime."""

from __future__ import annotations

from dataclasses import dataclass

from buzz.ai.provider import AIProvider
from buzz.core.planner import parse_plan
from buzz.core.request import BuzzRequest, BuzzResponse
from buzz.core.router import ToolRouter


SYSTEM_INSTRUCTION = """You are Buzz's planning brain. Return JSON only with keys reply and actions.
Each action is {"skill": string, "arguments": object, "reason": string}.
Never invent a skill. Available skills: {skills}.
If no tool is required, actions must be an empty array.
High-risk actions are still subject to Buzz's independent authorization layer."""


@dataclass
class BuzzRuntime:
    provider: AIProvider
    router: ToolRouter

    def handle(self, request: BuzzRequest, *, confirmed: bool = False) -> BuzzResponse:
        skills = ", ".join(self.router.registry.names()) or "(none)"
        prompt = SYSTEM_INSTRUCTION.format(skills=skills) + "\nUser request: " + request.text
        plan = parse_plan(self.provider.respond(prompt).text)
        results = []
        for action in plan.actions:
            result = self.router.execute(action.skill, confirmed=confirmed, **action.arguments)
            results.append({"skill": action.skill, "success": result.success, "message": result.message})
        return BuzzResponse(plan.reply, request.request_id, {"actions": results})
