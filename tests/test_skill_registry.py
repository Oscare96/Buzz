import pytest

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult
from buzz.skills.registry import SkillRegistry


class EchoSkill(Skill):
    name = "echo"
    description = "Return supplied text."
    risk_level = RiskLevel.READ

    def execute(self, **kwargs):
        return SkillResult(True, str(kwargs.get("text", "")))


def test_registry_registers_and_finds_skill():
    registry = SkillRegistry()
    registry.register(EchoSkill())
    assert registry.get("echo").name == "echo"
    assert registry.names() == ("echo",)


def test_registry_rejects_duplicate_skill():
    registry = SkillRegistry()
    registry.register(EchoSkill())
    with pytest.raises(ValueError):
        registry.register(EchoSkill())
