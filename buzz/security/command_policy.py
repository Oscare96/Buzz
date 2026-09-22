"""Execution policy metadata for Buzz capabilities."""
from dataclasses import dataclass
from buzz.security.risk import RiskLevel

@dataclass(frozen=True)
class ExecutionPolicy:
    risk: RiskLevel
    require_confirmation: bool = True

DEFAULT_POLICIES = {
    "read": ExecutionPolicy(RiskLevel.READ, False),
    "open": ExecutionPolicy(RiskLevel.LOW, False),
    "change": ExecutionPolicy(RiskLevel.CHANGE, True),
    "high": ExecutionPolicy(RiskLevel.HIGH, True),
    "critical": ExecutionPolicy(RiskLevel.CRITICAL, True),
}
