"""Smart-home gateway contract for Buzz."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HomeProvider(ABC):
    @abstractmethod
    def state(self, entity_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def call_service(self, domain: str, service: str, entity_id: str) -> dict[str, Any]:
        raise NotImplementedError
