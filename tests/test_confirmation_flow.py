from buzz.ai.provider import AIProvider, AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult
from buzz.skills.registry import SkillRegistry

class SensitiveSkill(Skill):
    name="test.sensitive"; description="test"; risk_level=RiskLevel.HIGH
    def execute(self, **kwargs): return SkillResult(True, "executed")

class FakeProvider(AIProvider):
    name="fake"
    def respond(self, message):
        return AIResponse('{"reply":"I can do that.","actions":[{"skill":"test.sensitive","arguments":{"value":1},"reason":"requested"}]}', self.name)

def test_sensitive_action_is_returned_as_pending():
    registry=SkillRegistry(); registry.register(SensitiveSkill())
    response=BuzzRuntime(FakeProvider(), ToolRouter(registry)).handle(BuzzRequest("do it"))
    assert response.metadata["pending_confirmation"][0]["skill"]=="test.sensitive"
