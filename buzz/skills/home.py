"""Executable smart-home skills with permission gating."""

from __future__ import annotations

from typing import Any

from buzz.integrations.home.base import HomeProvider
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class HomeStateSkill(Skill):
    name = "home.state"
    description = "Read the state of a smart-home entity."
    risk_level = RiskLevel.READ

    def __init__(self, provider: HomeProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        entity = str(kwargs.get("entity_id", "")).strip()
        if not entity: return SkillResult(False, "entity_id is required.")
        return SkillResult(True, "Home state retrieved.", self.provider.state(entity))


class HomeServiceSkill(Skill):
    name = "home.call_service"
    description = "Execute an authorized smart-home service."
    risk_level = RiskLevel.HIGH

    def __init__(self, provider: HomeProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        domain = str(kwargs.get("domain", "")).strip()
        service = str(kwargs.get("service", "")).strip()
        entity = str(kwargs.get("entity_id", "")).strip()
        if not all((domain, service, entity)): return SkillResult(False, "domain, service, and entity_id are required.")
        return SkillResult(True, "Home command executed.", self.provider.call_service(domain, service, entity, kwargs.get("data")))
