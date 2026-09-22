"""Local filesystem capabilities sandboxed to a configured Buzz workspace."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


def _workspace() -> Path:
    return Path(os.getenv("BUZZ_WORKSPACE", "~/BuzzWorkspace")).expanduser().resolve()


def _safe_path(value: Any) -> Path:
    raw = Path(str(value or ""))
    if not str(value or "").strip():
        raise ValueError("Path is required.")
    root = _workspace()
    candidate = (root / raw).resolve() if not raw.is_absolute() else raw.expanduser().resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Path must be inside Buzz workspace: {root}")
    return candidate


class ReadFileSkill(Skill):
    name = "filesystem.read"
    description = "Read a text file inside the configured Buzz workspace."
    risk_level = RiskLevel.READ
    argument_schema = {"type":"object","properties":{"path":{"type":"string","minLength":1,"maxLength":1024}},"required":["path"],"additionalProperties":False}
    def execute(self, **kwargs: Any) -> SkillResult:
        try:
            path = _safe_path(kwargs.get("path"))
            return SkillResult(True, "File read.", path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return SkillResult(False, f"Read failed: {exc}")


class WriteFileSkill(Skill):
    name = "filesystem.write"
    description = "Write a text file inside the Buzz workspace after authorization."
    risk_level = RiskLevel.HIGH
    argument_schema = {"type":"object","properties":{"path":{"type":"string","minLength":1,"maxLength":1024},"content":{"type":"string","maxLength":1000000}},"required":["path","content"],"additionalProperties":False}
    def execute(self, **kwargs: Any) -> SkillResult:
        try:
            path = _safe_path(kwargs.get("path"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(kwargs.get("content", "")), encoding="utf-8")
            return SkillResult(True, "File written.", {"path": str(path)})
        except (OSError, ValueError) as exc:
            return SkillResult(False, f"Write failed: {exc}")


class DeleteFileSkill(Skill):
    name = "filesystem.delete"
    description = "Delete a file inside the Buzz workspace after explicit authorization."
    risk_level = RiskLevel.CRITICAL
    argument_schema = {"type":"object","properties":{"path":{"type":"string"}},"required":["path"],"additionalProperties":False}
    def execute(self, **kwargs: Any) -> SkillResult:
        try:
            path = _safe_path(kwargs.get("path"))
            path.unlink()
            return SkillResult(True, "File deleted.", {"path": str(path)})
        except (OSError, ValueError) as exc:
            return SkillResult(False, f"Delete failed: {exc}")
