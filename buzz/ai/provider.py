"""Provider-neutral AI contracts for Buzz."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AIResponse:
    text: str
    provider: str
    model: str | None = None


class AIProvider(ABC):
    """Every cloud or local model adapter implements this interface."""

    name: str

    @abstractmethod
    def respond(self, message: str) -> AIResponse:
        raise NotImplementedError
