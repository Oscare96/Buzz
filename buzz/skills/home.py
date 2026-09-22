"""Executable smart-home skills with permission gating."""

from __future__ import annotations
from typing import Any
from buzz.integrations.home.base import HomeProvider
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult

class HomeStateSkill(Skill):
    name = "home.state"; description = "Read the state of a smart-home entity."; risk_level = RiskLevel.READ
    argument_schema = {"type":"object","properties":{"entity_id":{"type":"string"}},"required":["entity_id"],"additionalProperties":False}
    def __init__(self, provider: HomeProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        entity = str(kwargs.get("entity_id","")).strip()
        if not entity: return SkillResult(False,"entity_id is required.")
        return SkillResult(True,"Home state retrieved.",self.provider.state(entity))

class HomeServiceSkill(Skill):
    name = "home.call_service"; description = "Execute an authorized non-access-control smart-home service."; risk_level = RiskLevel.HIGH
    argument_schema = {"type":"object","properties":{"domain":{"type":"string"},"service":{"type":"string"},"entity_id":{"type":"string"},"data":{"type":"object"}},"required":["domain","service","entity_id"],"additionalProperties":False}
    def __init__(self, provider: HomeProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        domain = str(kwargs.get("domain","")).strip(); service = str(kwargs.get("service","")).strip(); entity = str(kwargs.get("entity_id","")).strip()
        if not all((domain,service,entity)): return SkillResult(False,"domain, service, and entity_id are required.")
        if domain in {"lock","cover"}: return SkillResult(False,"Access-control devices require home.access_control.")
        return SkillResult(True,"Home command executed.",self.provider.call_service(domain,service,entity,kwargs.get("data")))

class HomeAccessControlSkill(Skill):
    name = "home.access_control"; description = "Operate a lock, door, or garage after critical authorization."; risk_level = RiskLevel.CRITICAL
    argument_schema = {"type":"object","properties":{"domain":{"type":"string","enum":["lock","cover"]},"service":{"type":"string"},"entity_id":{"type":"string"}},"required":["domain","service","entity_id"],"additionalProperties":False}
    def __init__(self, provider: HomeProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        domain = str(kwargs.get("domain","")).strip(); service = str(kwargs.get("service","")).strip(); entity = str(kwargs.get("entity_id","")).strip()
        if domain not in {"lock","cover"} or not service or not entity: return SkillResult(False,"Valid access-control domain, service, and entity_id are required.")
        return SkillResult(True,"Access-control command executed.",self.provider.call_service(domain,service,entity,None))
