"""Build the default trusted Buzz skill registry."""

from buzz.skills.computer import OpenApplicationSkill, OpenUrlSkill
from buzz.skills.registry import SkillRegistry
from buzz.skills.system import SystemInfoSkill


def build_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    for skill in (SystemInfoSkill(), OpenUrlSkill(), OpenApplicationSkill()):
        registry.register(skill)
    return registry
