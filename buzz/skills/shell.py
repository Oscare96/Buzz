"""Local command execution capability for Buzz."""

from __future__ import annotations

import subprocess
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class ShellCommandSkill(Skill):
    name = "computer.run_command"
    description = "Run an explicitly authorized local command without using a shell interpreter."
    risk_level = RiskLevel.CRITICAL
    argument_schema = {"type":"object","properties":{"argv":{"type":"array","items":{"type":"string"}},"cwd":{"type":["string","null"]}},"required":["argv"],"additionalProperties":False}

    def execute(self, **kwargs: Any) -> SkillResult:
        argv = kwargs.get("argv")
        cwd = kwargs.get("cwd")
        if not isinstance(argv, list) or not argv or not all(isinstance(v, str) and v for v in argv):
            return SkillResult(False, "argv must be a non-empty list of command arguments.")
        try:
            result = subprocess.run(argv, cwd=cwd or None, capture_output=True, text=True, timeout=120, shell=False)
        except (OSError, subprocess.SubprocessError) as exc:
            return SkillResult(False, f"Command failed to run: {exc}")
        data = {"returncode": result.returncode, "stdout": result.stdout[-12000:], "stderr": result.stderr[-12000:]}
        return SkillResult(result.returncode == 0, f"Command exited with code {result.returncode}.", data)
