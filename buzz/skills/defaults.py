"""Build the default trusted Buzz skill registry."""

from buzz.config.settings import Settings
from buzz.integrations.home_assistant import HomeAssistantProvider
from buzz.skills.computer import OpenApplicationSkill, OpenUrlSkill
from buzz.skills.filesystem import DeleteFileSkill, ReadFileSkill, WriteFileSkill
from buzz.skills.home import HomeAccessControlSkill, HomeServiceSkill, HomeStateSkill
from buzz.skills.registry import SkillRegistry
from buzz.skills.shell import ShellCommandSkill
from buzz.skills.system import SystemInfoSkill


def build_default_registry(settings: Settings | None = None) -> SkillRegistry:
    registry = SkillRegistry()
    for skill in (SystemInfoSkill(), OpenUrlSkill(), OpenApplicationSkill(), ReadFileSkill(), WriteFileSkill(), DeleteFileSkill(), ShellCommandSkill()):
        registry.register(skill)
    if settings and settings.home_assistant_enabled:
        provider = HomeAssistantProvider(settings.home_assistant_url, settings.home_assistant_token)
        for skill in (HomeStateSkill(provider), HomeServiceSkill(provider), HomeAccessControlSkill(provider)):
            registry.register(skill)
    return registry
