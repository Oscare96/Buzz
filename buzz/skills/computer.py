"""Low-risk local computer capabilities for Buzz."""

from __future__ import annotations

import os
import subprocess
import webbrowser
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


DEFAULT_APPLICATIONS = {
    "chrome": "chrome.exe",
    "cursor": "Cursor.exe",
    "notepad": "notepad.exe",
    "spotify": "Spotify.exe",
    "vscode": "code.exe",
}


class OpenUrlSkill(Skill):
    name = "computer.open_url"
    description = "Open an http or https URL in the default browser."
    risk_level = RiskLevel.LOW
    argument_schema = {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"], "additionalProperties": False}

    def execute(self, **kwargs: Any) -> SkillResult:
        url = str(kwargs.get("url", "")).strip()
        if not url.startswith(("https://", "http://")):
            return SkillResult(False, "Only http/https URLs are allowed.")
        opened = webbrowser.open(url)
        return SkillResult(bool(opened), f"Opened {url}" if opened else f"Could not open {url}")


class OpenApplicationSkill(Skill):
    name = "computer.open_application"
    description = "Launch an application from Buzz's approved application catalog."
    risk_level = RiskLevel.LOW
    argument_schema = {"type": "object", "properties": {"app": {"type": "string"}}, "required": ["app"], "additionalProperties": False}

    def __init__(self, applications: dict[str, str] | None = None) -> None:
        self.applications = {**DEFAULT_APPLICATIONS, **(applications or {})}

    def execute(self, **kwargs: Any) -> SkillResult:
        app = str(kwargs.get("app", "")).strip().lower()
        executable = self.applications.get(app)
        if not executable:
            return SkillResult(False, f"Application '{app}' is not in the approved catalog.")
        try:
            subprocess.Popen([os.path.expandvars(executable)], shell=False)
        except OSError as exc:
            return SkillResult(False, f"Launch failed: {exc}")
        return SkillResult(True, f"Launched {app}.")
