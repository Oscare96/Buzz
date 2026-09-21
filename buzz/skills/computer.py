"""Low-risk local computer capabilities for Buzz."""

from __future__ import annotations

import subprocess
import sys
import webbrowser
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class OpenUrlSkill(Skill):
    name = "computer.open_url"
    description = "Open an http or https URL in the default browser."
    risk_level = RiskLevel.LOW

    def execute(self, **kwargs: Any) -> SkillResult:
        url = str(kwargs.get("url", "")).strip()
        if not url.startswith(("https://", "http://")):
            return SkillResult(False, "Only http/https URLs are allowed.")
        opened = webbrowser.open(url)
        return SkillResult(bool(opened), f"Opened {url}" if opened else f"Could not open {url}")


class OpenApplicationSkill(Skill):
    name = "computer.open_application"
    description = "Launch an explicitly named local application."
    risk_level = RiskLevel.LOW

    def execute(self, **kwargs: Any) -> SkillResult:
        executable = str(kwargs.get("executable", "")).strip()
        if not executable:
            return SkillResult(False, "Executable is required.")
        try:
            if sys.platform == "win32":
                subprocess.Popen([executable], shell=False)
            else:
                subprocess.Popen([executable])
        except OSError as exc:
            return SkillResult(False, f"Launch failed: {exc}")
        return SkillResult(True, f"Launched {executable}")
