"""Continuous wake-word-driven Buzz assistant."""

from __future__ import annotations

from time import sleep

from buzz.voice.voice_loop import VoiceLoop
from buzz.voice.wake_word import WakeWordDetector


class VoiceAssistant:
    def __init__(self, detector: WakeWordDetector, loop: VoiceLoop) -> None:
        self.detector = detector
        self.loop = loop

    def run(self) -> None:
        self.detector.start()
        try:
            while True:
                if self.detector.detected():
                    self.detector.stop()
                    try:
                        self.loop.conversation()
                    finally:
                        self.detector.start()
                sleep(0.05)
        finally:
            self.detector.stop()
