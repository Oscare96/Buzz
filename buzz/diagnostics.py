"""Local preflight checks before the first Buzz PC test."""
from __future__ import annotations
import os
import platform
import sys
from pathlib import Path
from buzz.config.settings import Settings
from buzz.status import status_report


def self_check(settings: Settings | None = None) -> dict:
    settings=settings or Settings.load()
    workspace=Path(os.path.expanduser(os.getenv("BUZZ_WORKSPACE","~/BuzzWorkspace")))
    checks=[]
    checks.append({"name":"python","ok":sys.version_info >= (3,11),"detail":platform.python_version()})
    try:
        workspace.mkdir(parents=True,exist_ok=True)
        probe=workspace/".buzz-write-test"
        probe.write_text("ok",encoding="utf-8"); probe.unlink()
        checks.append({"name":"workspace","ok":True,"detail":str(workspace)})
    except OSError as exc:
        checks.append({"name":"workspace","ok":False,"detail":str(exc)})
    capabilities=status_report(settings)
    checks.append({"name":"core_skills","ok":len(capabilities["skills"])>=4,"detail":", ".join(capabilities["skills"])})
    checks.append({"name":"openai_key","ok":bool(settings.openai_api_key),"detail":"configured" if settings.openai_api_key else "missing"})
    checks.append({"name":"platform","ok":True,"detail":platform.platform()})
    checks.append({"name":"api_token","ok":bool(settings.api_token),"detail":"configured" if settings.api_token else "missing (required before API/mobile control)"})
    return {"ready_for_core_test":all(c["ok"] for c in checks if c["name"] not in {"openai_key","api_token"}) and bool(settings.openai_api_key),"checks":checks,"capabilities":capabilities}
