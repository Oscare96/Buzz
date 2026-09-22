"""Safe in-memory trading provider for development and tests."""
from typing import Any
from buzz.integrations.trading.base import TradingProvider

class MockTradingProvider(TradingProvider):
    def __init__(self) -> None:
        self.orders: list[dict[str, Any]] = []
        self.bots: dict[str, bool] = {}
    def portfolio(self): return {"equity": 0.0, "positions": []}
    def bot_status(self): return {"bots": self.bots.copy()}
    def preview_order(self, symbol, side, quantity): return {"symbol":symbol,"side":side,"quantity":quantity,"status":"preview"}
    def place_order(self, symbol, side, quantity, idempotency_key):
        order={"symbol":symbol,"side":side,"quantity":quantity,"idempotency_key":idempotency_key,"status":"accepted"}
        self.orders.append(order); return order
    def set_bot_enabled(self, bot, enabled): self.bots[bot]=enabled; return {"bot":bot,"enabled":enabled}
