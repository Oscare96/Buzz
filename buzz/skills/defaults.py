"""Build the default trusted Buzz skill registry."""

from buzz.config.settings import Settings
from buzz.integrations.home_assistant import HomeAssistantProvider
from buzz.integrations.trading.alpaca import AlpacaTradingProvider
from buzz.integrations.devops.github import GitHubDevOpsProvider
from buzz.skills.computer import OpenApplicationSkill, OpenUrlSkill
from buzz.skills.devops import PipelineFailureSkill, PipelineStatusSkill
from buzz.skills.devops_execute import RunPipelineSkill
from buzz.skills.filesystem import DeleteFileSkill, ReadFileSkill, WriteFileSkill
from buzz.skills.home import HomeAccessControlSkill, HomeServiceSkill, HomeStateSkill
from buzz.skills.registry import SkillRegistry
from buzz.skills.shell import ShellCommandSkill
from buzz.skills.system import SystemInfoSkill
from buzz.skills.trading import PlaceOrderSkill, PortfolioSkill, PreviewOrderSkill


def build_default_registry(settings: Settings | None = None) -> SkillRegistry:
    registry = SkillRegistry()
    for skill in (SystemInfoSkill(), OpenUrlSkill(), OpenApplicationSkill(), ReadFileSkill(), WriteFileSkill(), DeleteFileSkill(), ShellCommandSkill()):
        registry.register(skill)
    if settings and settings.alpaca_enabled:
        trading = AlpacaTradingProvider(settings.alpaca_api_key, settings.alpaca_secret_key, settings.alpaca_base_url)
        registry.register(PortfolioSkill(trading))
        registry.register(PreviewOrderSkill(trading))
        # Broker execution is intentionally limited to Alpaca paper trading until live mode is explicitly enabled.
        if settings.alpaca_paper_enabled:
            registry.register(PlaceOrderSkill(trading))
    if settings and settings.github_enabled:
        github = GitHubDevOpsProvider(settings.github_token)
        registry.register(PipelineStatusSkill(github))
        registry.register(PipelineFailureSkill(github))
        registry.register(RunPipelineSkill(github))
    if settings and settings.home_assistant_enabled:
        provider = HomeAssistantProvider(settings.home_assistant_url, settings.home_assistant_token)
        for skill in (HomeStateSkill(provider), HomeServiceSkill(provider), HomeAccessControlSkill(provider)):
            registry.register(skill)
    return registry
