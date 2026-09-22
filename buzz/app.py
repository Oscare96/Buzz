"""Buzz application composition root."""

from __future__ import annotations

from pathlib import Path

from buzz.ai.openai_provider import OpenAIProvider
from buzz.config.settings import Settings
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.audit_log import AuditLog
from buzz.skills.defaults import build_default_registry
from buzz.memory.json_store import JsonMemoryStore


def build_runtime() -> BuzzRuntime:
    settings = Settings.load()
    settings.validate_ai()
    router = ToolRouter(build_default_registry(settings), AuditLog(Path(".cache/buzz/audit.jsonl")))
    return BuzzRuntime(provider=OpenAIProvider(), router=router, memory=JsonMemoryStore())
