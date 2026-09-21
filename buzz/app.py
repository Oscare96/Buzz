"""Buzz application composition root."""

from __future__ import annotations

from buzz.ai.openai_provider import OpenAIProvider
from buzz.config.settings import Settings
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.skills.defaults import build_default_registry


def build_runtime() -> BuzzRuntime:
    settings = Settings.load()
    settings.validate_ai()
    return BuzzRuntime(provider=OpenAIProvider(), router=ToolRouter(build_default_registry()))
