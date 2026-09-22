import sys,types
from buzz.ai.openai_provider import OpenAIProvider

class Responses:
    def __init__(self): self.kwargs=None
    def create(self,**kwargs):
        self.kwargs=kwargs
        return types.SimpleNamespace(output_text='{"reply":"ok","actions":[]}')
class Client:
    def __init__(self,**kwargs): self.responses=Responses()

def test_openai_provider_requests_strict_json_schema(monkeypatch):
    client=Client()
    monkeypatch.setitem(sys.modules,"openai",types.SimpleNamespace(OpenAI=lambda **kwargs:client))
    monkeypatch.setenv("OPENAI_API_KEY","test")
    provider=OpenAIProvider(model="test-model")
    response=provider.respond("hello")
    assert response.text.startswith("{")
    fmt=client.responses.kwargs["text"]["format"]
    assert fmt["type"]=="json_schema" and fmt["strict"] is True
    assert client.responses.kwargs["model"]=="test-model"
