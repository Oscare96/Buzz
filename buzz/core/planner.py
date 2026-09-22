"""Convert model output into validated Buzz action plans."""

from __future__ import annotations

import json
from typing import Any

from buzz.core.actions import ActionPlan, PlannedAction


class PlanError(ValueError):
    pass


def parse_plan(raw: str) -> ActionPlan:
    try:
        payload: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PlanError("AI response was not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise PlanError("AI plan must be a JSON object.")
    reply = payload.get("reply", "")
    actions = payload.get("actions", [])
    if not isinstance(reply, str) or not isinstance(actions, list):
        raise PlanError("AI plan has invalid reply/actions fields.")
    if len(actions)>16:
        raise PlanError("AI plan contains too many actions.")
    if len(reply)>12000:
        raise PlanError("AI reply is too large.")
    parsed = []
    for item in actions:
        if not isinstance(item, dict) or not isinstance(item.get("skill"), str) or not item.get("skill").strip() or len(item.get("skill",""))>128:
            raise PlanError("Each action requires a skill name.")
        arguments = item.get("arguments", {})
        if not isinstance(arguments, dict):
            raise PlanError("Action arguments must be an object.")
        parsed.append(PlannedAction(item["skill"], arguments, str(item.get("reason", ""))))
    return ActionPlan(reply=reply, actions=tuple(parsed))
