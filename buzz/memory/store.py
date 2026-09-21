"""Memory interface kept separate from operational state and secrets."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MemoryStore(ABC):
    @abstractmethod
    def put(self, namespace: str, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, namespace: str, key: str) -> Any | None:
        raise NotImplementedError


class InMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._data: dict[tuple[str, str], Any] = {}

    def put(self, namespace: str, key: str, value: Any) -> None:
        self._data[(namespace, key)] = value

    def get(self, namespace: str, key: str) -> Any | None:
        return self._data.get((namespace, key))
