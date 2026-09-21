from buzz.ai.provider import AIProvider, AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult
from buzz.skills.registry import SkillRegistry

class ChangeSkill(Skill):
    name = "test.change"; description = "test"; risk_level = RiskLevel.HIGH
    def execute(self, **kwargs): return SkillResult(True, "changed", kwargs)

class Planner(AIProvider):
    name = "test"
    def respond(self, message): return AIResponse('{"reply":"","actions":[{"skill":"test.change","arguments":{"target":"a"},"reason":"test"}]}', self.name)

def test_approval_rejects_argument_change():
    registry = SkillRegistry(); registry.register(ChangeSkill())
    runtime = BuzzRuntime(Planner(), ToolRouter(registry))
    pending = runtime.handle(BuzzRequest("change")).metadata["pending_confirmation"][0]
    result = runtime.confirm(pending["skill"], {"target":"b"}, pending["approval_token"])
    assert not result.success
