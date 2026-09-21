"""Local filesystem capabilities with destructive actions gated."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class ReadFileSkill(Skill):
    name = "filesystem.read"
    description = "Read a local text file."
    risk_level = RiskLevel.READ
    def execute(self, **kwargs: Any) -> SkillResult:
        path = Path(str(kwargs.get("path", ""))).expanduser()
        try: return SkillResult(True, "File read.", path.read_text(encoding="utf-8"))
        except OSError as exc: return SkillResult(False, f"Read failed: {exc}")


class WriteFileSkill(Skill):
    name = "filesystem.write"
    description = "Write a local text file after authorization."
    risk_level = RiskLevel.HIGH
    def execute(self, **kwargs: Any) -> SkillResult:
        path = Path(str(kwargs.get("path", ""))).expanduser()
        content = str(kwargs.get("content", ""))
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return SkillResult(True, "File written.")
        except OSError as exc: return SkillResult(False, f"Write failed: {exc}")


class DeleteFileSkill(Skill):
    name = "filesystem.delete"
    description = "Delete a local file only after explicit authorization."
    risk_level = RiskLevel.CRITICAL
    def execute(self, **kwargs: Any) -> SkillResult:
        path = Path(str(kwargs.get("path", ""))).expanduser()
        try:
            path.unlink()
            return SkillResult(True, "File deleted.")
        except OSError as exc: return SkillResult(False, f"Delete failed: {exc}")
