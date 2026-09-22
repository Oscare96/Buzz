from buzz.core.router import ToolRouter
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult
from buzz.skills.registry import SkillRegistry


class DangerousSkill(Skill):
    name = "danger"
    description = "Test high-risk action."
    risk_level = RiskLevel.CRITICAL

    def execute(self, **kwargs):
        return SkillResult(True, "executed")


def test_router_blocks_unconfirmed_critical_action():
    registry = SkillRegistry()
    registry.register(DangerousSkill())
    result = ToolRouter(registry).execute("danger")
    assert not result.success


def test_router_allows_confirmed_critical_action():
    registry = SkillRegistry()
    registry.register(DangerousSkill())
    result = ToolRouter(registry).execute("danger", confirmed=True)
    assert result.success
