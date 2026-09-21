"""Provider-neutral contracts for DevOps systems."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DevOpsProvider(ABC):
    @abstractmethod
    def repository_status(self, repository: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def pipeline_status(self, repository: str) -> dict[str, Any]:
        raise NotImplementedError
