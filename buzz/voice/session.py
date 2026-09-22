"""Conversation session state for Buzz voice interactions."""

from dataclasses import dataclass
from time import monotonic


@dataclass
class VoiceSession:
    timeout_seconds: float = 20.0
    active: bool = False
    last_activity: float = 0.0

    def activate(self) -> None:
        self.active = True
        self.touch()

    def touch(self) -> None:
        self.last_activity = monotonic()

    def deactivate(self) -> None:
        self.active = False

    def expired(self) -> bool:
        if not self.active:
            return True
        return monotonic() - self.last_activity >= self.timeout_seconds
