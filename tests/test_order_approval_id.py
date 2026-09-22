import json
from buzz.ai.provider import AIProvider,AIResponse
from buzz.core.request import BuzzRequest
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.integrations.trading.mock import MockTradingProvider
from buzz.skills.registry import SkillRegistry
from buzz.skills.trading import PlaceOrderSkill

class Planner(AIProvider):
    def respond(self,message):
        return AIResponse(json.dumps({"reply":"Ready.","actions":[{"skill":"trading.place_order","arguments":{"symbol":"AAPL","side":"buy","quantity":1},"reason":"requested"}]}),"test")

def test_order_id_is_bound_before_confirmation():
    registry=SkillRegistry(); registry.register(PlaceOrderSkill(MockTradingProvider()))
    pending=BuzzRuntime(Planner(),ToolRouter(registry)).handle(BuzzRequest("buy")).metadata["pending_confirmation"][0]
    assert pending["arguments"]["idempotency_key"]
