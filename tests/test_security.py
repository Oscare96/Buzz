from buzz.security.policy import authorize
from buzz.security.risk import RiskLevel


def test_read_action_is_allowed():
    decision = authorize(RiskLevel.READ)
    assert decision.allowed
    assert not decision.requires_confirmation


def test_critical_action_requires_confirmation():
    decision = authorize(RiskLevel.CRITICAL)
    assert not decision.allowed
    assert decision.requires_confirmation


def test_confirmed_critical_action_is_allowed():
    decision = authorize(RiskLevel.CRITICAL, confirmed=True)
    assert decision.allowed
