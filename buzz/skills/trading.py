"""Read-only trading skills; execution remains separately gated."""

from __future__ import annotations

from typing import Any

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
