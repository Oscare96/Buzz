from buzz.ai.provider import AIProvider, AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult
from buzz.skills.registry import SkillRegistry

class ChangeSkill(Skill):
    name = "test.change"
    description = "test change"
    risk_level = RiskLevel.HIGH
    def execute(self, **kwargs):
        return SkillResult(True, "changed", kwargs)

class Planner(AIProvider):
    name = "test"
    def respond(self, message):
        return AIResponse('{"reply":"Ready.","actions":[{"skill":"test.change","arguments":{"target":"demo"},"reason":"user asked"}]}', self.name)

def test_runtime_blocks_then_allows_exact_sensitive_action():
    registry = SkillRegistry(); registry.register(ChangeSkill())
    runtime = BuzzRuntime(Planner(), ToolRouter(registry))
    response = runtime.handle(BuzzRequest("change demo"))
    pending = response.metadata["pending_confirmation"]
    assert pending and pending[0]["arguments"] == {"target":"demo"}
    result = runtime.confirm(pending[0]["skill"], pending[0]["arguments"], pending[0]["approval_token"])
    assert result.success and result.data["verified"] is True
    assert result.data["result"]["target"] == "demo"
