"""Text-to-speech contracts for Buzz."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Immediately stop playback for barge-in commands."""
        raise NotImplementedError
