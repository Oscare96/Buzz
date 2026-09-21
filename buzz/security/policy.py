"""Default-deny authorization policy for Buzz actions."""

from dataclasses import dataclass

from buzz.security.risk import RiskLevel


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    requires_confirmation: bool
    reason: str


def authorize(risk: RiskLevel, confirmed: bool = False) -> AuthorizationDecision:
    if risk <= RiskLevel.LOW:
        return AuthorizationDecision(True, False, "Low-risk action allowed.")
    if confirmed:
        return AuthorizationDecision(True, False, "User confirmation received.")
    return AuthorizationDecision(False, True, "Confirmation required before execution.")
