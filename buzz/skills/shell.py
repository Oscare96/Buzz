"""Local command execution capability for Buzz."""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
from typing import Any
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult

def _workspace() -> Path:
    return Path(os.getenv("BUZZ_WORKSPACE","~/BuzzWorkspace")).expanduser().resolve()

def _safe_cwd(value: Any) -> Path:
    root=_workspace()
    if value is None or not str(value).strip(): return root
    raw=Path(str(value)).expanduser()
    candidate=(root/raw).resolve() if not raw.is_absolute() else raw.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Working directory must be inside Buzz workspace: {root}")
    return candidate

class ShellCommandSkill(Skill):
    name="computer.run_command"
    description="Run an explicitly authorized local command without using a shell interpreter."
    risk_level=RiskLevel.CRITICAL
    argument_schema={"type":"object","properties":{"argv":{"type":"array","items":{"type":"string"},"minItems":1,"maxItems":64},"cwd":{"type":["string","null"]}},"required":["argv"],"additionalProperties":False}
    def execute(self, **kwargs: Any) -> SkillResult:
        argv=kwargs.get("argv")
        if not isinstance(argv,list) or not argv or not all(isinstance(v,str) and v for v in argv):
            return SkillResult(False,"argv must be a non-empty list of command arguments.")
        try:
            cwd=_safe_cwd(kwargs.get("cwd")); cwd.mkdir(parents=True,exist_ok=True)
            result=subprocess.run(argv,cwd=str(cwd),capture_output=True,text=True,timeout=120,shell=False)
        except (OSError,ValueError,subprocess.SubprocessError) as exc:
            return SkillResult(False,f"Command failed to run: {exc}")
        data={"returncode":result.returncode,"stdout":result.stdout[-12000:],"stderr":result.stderr[-12000:],"cwd":str(cwd)}
        return SkillResult(result.returncode==0,f"Command exited with code {result.returncode}.",data)
