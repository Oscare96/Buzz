import json
from buzz.ai.provider import AIProvider,AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill,SkillResult
from buzz.skills.registry import SkillRegistry

class Provider(AIProvider):
    def respond(self,message):
        return AIResponse(json.dumps({"reply":"ok","actions":[{"skill":"counter","arguments":{},"reason":"x"},{"skill":"counter","arguments":{},"reason":"x"}]}),"test")
class Counter(Skill):
    name="counter"; description="counter"; risk=RiskLevel.READ
    def __init__(self): self.calls=0
    def execute(self,**kwargs): self.calls+=1; return SkillResult(True,"ok")

def test_duplicate_actions_execute_once():
    skill=Counter(); registry=SkillRegistry(); registry.register(skill)
    response=BuzzRuntime(Provider(),ToolRouter(registry)).handle(BuzzRequest("go"))
    assert skill.calls==1
    assert response.metadata["actions"][1]["message"]=="Duplicate action skipped."
