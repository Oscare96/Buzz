"""Wake-word contracts for Buzz."""

from __future__ import annotations

from abc import ABC, abstractmethod


class WakeWordDetector(ABC):
    """Detect a local activation phrase without coupling Buzz to one engine."""

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def detected(self) -> bool:
        raise NotImplementedError
