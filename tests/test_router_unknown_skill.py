from buzz.core.router import ToolRouter
from buzz.skills.registry import SkillRegistry

def test_unknown_skill_returns_failure_instead_of_crashing():
    result=ToolRouter(SkillRegistry()).execute("missing.skill")
    assert result.success is False
    assert "Unknown skill" in result.message
    assert result.data["execution_id"]
