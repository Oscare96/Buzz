"""Build the default trusted Buzz skill registry."""

from buzz.skills.computer import OpenApplicationSkill, OpenUrlSkill
from buzz.skills.filesystem import DeleteFileSkill, ReadFileSkill, WriteFileSkill
from buzz.skills.registry import SkillRegistry
from buzz.skills.system import SystemInfoSkill


def build_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    for skill in (
        SystemInfoSkill(), OpenUrlSkill(), OpenApplicationSkill(),
        ReadFileSkill(), WriteFileSkill(), DeleteFileSkill(),
    ):
        registry.register(skill)
    return registry
