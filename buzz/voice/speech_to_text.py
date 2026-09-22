"""Speech-to-text contracts for Buzz."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Transcript:
    text: str
    language: str | None = None


class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path) -> Transcript:
        raise NotImplementedError
