"""Post-execution verification helpers for Buzz."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    message: str
    data: Any = None

Verifier = Callable[[Any], VerificationResult]

def verify_success(result: Any) -> VerificationResult:
    success = bool(getattr(result, "success", False))
    return VerificationResult(success, "Execution verified." if success else "Execution was not successful.", getattr(result, "data", None))
