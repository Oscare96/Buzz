"""Executable DevOps skills with explicit risk levels."""

from __future__ import annotations

from typing import Any

from buzz.integrations.devops.base import DevOpsProvider
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class RunPipelineSkill(Skill):
    name = "devops.run_pipeline"
    description = "Start a CI/CD workflow after authorization."
    risk_level = RiskLevel.HIGH
    argument_schema = {"type":"object","properties":{"repository":{"type":"string"},"workflow":{"type":"string"},"ref":{"type":"string"}},"required":["repository","workflow","ref"],"additionalProperties":False}

    def __init__(self, provider: DevOpsProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        repo, workflow, ref = (str(kwargs.get(k, "")).strip() for k in ("repository", "workflow", "ref"))
        if not all((repo, workflow, ref)): return SkillResult(False, "repository, workflow, and ref are required.")
        return SkillResult(True, "Pipeline started.", self.provider.run_pipeline(repo, workflow, ref))


class DeploySkill(Skill):
    name = "devops.deploy"
    description = "Deploy an application to an environment after explicit authorization."
    risk_level = RiskLevel.CRITICAL
    argument_schema = {"type":"object","properties":{"application":{"type":"string"},"environment":{"type":"string"},"version":{"type":"string"}},"required":["application","environment","version"],"additionalProperties":False}

    def __init__(self, provider: DevOpsProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        app, env, version = (str(kwargs.get(k, "")).strip() for k in ("application", "environment", "version"))
        if not all((app, env, version)): return SkillResult(False, "application, environment, and version are required.")
        return SkillResult(True, "Deployment requested.", self.provider.deploy(app, env, version))


class RemoteCommandSkill(Skill):
    name = "devops.run_command"
    description = "Run an authorized command on an approved DevOps target."
    risk_level = RiskLevel.CRITICAL
    argument_schema = {"type":"object","properties":{"target":{"type":"string"},"command":{"type":"string"}},"required":["target","command"],"additionalProperties":False}

    def __init__(self, provider: DevOpsProvider) -> None: self.provider = provider
    def execute(self, **kwargs: Any) -> SkillResult:
        target = str(kwargs.get("target", "")).strip()
        command = str(kwargs.get("command", "")).strip()
        if not target or not command: return SkillResult(False, "target and command are required.")
        return SkillResult(True, "Remote command executed.", self.provider.run_command(target, command))
