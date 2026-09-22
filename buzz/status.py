"""Local Buzz capability status without requiring an AI provider."""
from __future__ import annotations
from buzz.config.settings import Settings
from buzz.skills.defaults import build_default_registry

def status_report(settings: Settings | None = None) -> dict:
    settings=settings or Settings.load()
    registry=build_default_registry(settings)
    return {
        "ai_configured": bool(settings.openai_api_key),
        "voice_configured": bool(settings.openai_api_key and settings.elevenlabs_api_key and settings.elevenlabs_voice_id and settings.wake_model),
        "wake_model_configured": bool(settings.wake_model),
        "github_configured": settings.github_enabled,
        "home_assistant_configured": settings.home_assistant_enabled,
        "alpaca_configured": settings.alpaca_enabled,
        "alpaca_paper_execution": settings.alpaca_paper_enabled,
        "api_control_configured": bool(settings.api_token),
        "skills": registry.names(),
    }
