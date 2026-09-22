from buzz.security.risk import RiskLevel
from buzz.skills.defaults import build_default_registry


def test_shell_execution_is_registered_as_critical():
    skill = build_default_registry().get("computer.run_command")
    assert skill.risk_level == RiskLevel.CRITICAL
