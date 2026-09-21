"""Read-only DevOps skills."""

from __future__ import annotations

from typing import Any

from buzz.integrations.devops.base import DevOpsProvider
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class PipelineStatusSkill(Skill):
    name = "devops.pipeline_status"
    description = "Read CI/CD pipeline status for a repository."
    risk_level = RiskLevel.READ
    argument_schema = {"type":"object","properties":{"repository":{"type":"string"}},"required":["repository"],"additionalProperties":False}

    def __init__(self, provider: DevOpsProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        repository = str(kwargs.get("repository", "")).strip()
        if not repository:
            return SkillResult(False, "Repository is required.")
        return SkillResult(True, "Pipeline status retrieved.", self.provider.pipeline_status(repository))


class PipelineFailureSkill(Skill):
    name = "devops.pipeline_failure"
    description = "Inspect the latest failed CI/CD run and identify failed jobs and steps."
    risk_level = RiskLevel.READ
    argument_schema = {"type":"object","properties":{"repository":{"type":"string"}},"required":["repository"],"additionalProperties":False}

    def __init__(self, provider: DevOpsProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        repository = str(kwargs.get("repository","")).strip()
        if not repository: return SkillResult(False,"Repository is required.")
        return SkillResult(True,"Pipeline failure inspected.",self.provider.pipeline_failure(repository))
