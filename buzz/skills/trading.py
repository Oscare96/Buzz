"""Trading skills with explicit risk classifications."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from buzz.integrations.trading.base import TradingProvider
from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class PortfolioSkill(Skill):
    name = "trading.portfolio"
    description = "Read the connected trading portfolio."
    risk_level = RiskLevel.READ

    def __init__(self, provider: TradingProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        return SkillResult(True, "Portfolio retrieved.", self.provider.portfolio())


class BotStatusSkill(Skill):
    name = "trading.bot_status"
    description = "Read trading bot status without changing it."
    risk_level = RiskLevel.READ

    def __init__(self, provider: TradingProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        return SkillResult(True, "Trading bot status retrieved.", self.provider.bot_status())


class PreviewOrderSkill(Skill):
    name = "trading.preview_order"
    description = "Preview a proposed order without sending it to the broker."
    risk_level = RiskLevel.READ

    def __init__(self, provider: TradingProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        symbol, side, quantity = _order_args(kwargs)
        return SkillResult(True, "Order preview generated.", self.provider.preview_order(symbol, side, quantity))


class PlaceOrderSkill(Skill):
    name = "trading.place_order"
    description = "Place a broker order only after Buzz authorization and explicit user confirmation."
    risk_level = RiskLevel.CRITICAL

    def __init__(self, provider: TradingProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        symbol, side, quantity = _order_args(kwargs)
        key = str(kwargs.get("idempotency_key") or uuid4().hex)
        data = self.provider.place_order(symbol, side, quantity, key)
        return SkillResult(True, "Order submitted to broker.", data)


class SetBotEnabledSkill(Skill):
    name = "trading.set_bot_enabled"
    description = "Pause or resume a trading bot after user confirmation."
    risk_level = RiskLevel.HIGH

    def __init__(self, provider: TradingProvider) -> None:
        self.provider = provider

    def execute(self, **kwargs: Any) -> SkillResult:
        bot = str(kwargs.get("bot", "")).strip()
        enabled = kwargs.get("enabled")
        if not bot or not isinstance(enabled, bool):
            return SkillResult(False, "Bot name and boolean enabled value are required.")
        return SkillResult(True, "Trading bot state changed.", self.provider.set_bot_enabled(bot, enabled))


def _order_args(kwargs: dict[str, Any]) -> tuple[str, str, float]:
    symbol = str(kwargs.get("symbol", "")).strip().upper()
    side = str(kwargs.get("side", "")).strip().lower()
    try:
        quantity = float(kwargs.get("quantity", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("Quantity must be numeric.") from exc
    if not symbol or side not in {"buy", "sell"} or quantity <= 0:
        raise ValueError("A symbol, buy/sell side, and positive quantity are required.")
    return symbol, side, quantity
