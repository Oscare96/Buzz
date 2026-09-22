from buzz.ai.provider import AIProvider,AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.skills.registry import SkillRegistry

class BadProvider(AIProvider):
    def respond(self,message): return AIResponse("not-json","test")

def test_bad_ai_plan_does_not_crash_runtime():
    response=BuzzRuntime(BadProvider(),ToolRouter(SkillRegistry())).handle(BuzzRequest("hello"))
    assert response.metadata["plan_error"] is True
    assert response.metadata["actions"]==[]
