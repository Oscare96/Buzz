from buzz.ai.provider import AIProvider, AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.skills.defaults import build_default_registry


class FakeProvider(AIProvider):
    name = "fake"

    def respond(self, message: str) -> AIResponse:
        return AIResponse('{"reply":"Checking.","actions":[{"skill":"system.info","arguments":{},"reason":"requested"}]}', self.name)


def test_runtime_executes_planned_read_skill():
    runtime = BuzzRuntime(FakeProvider(), ToolRouter(build_default_registry()))
    response = runtime.handle(BuzzRequest("system status"))
    assert response.text == "Checking."
    assert response.metadata["actions"][0]["success"]
