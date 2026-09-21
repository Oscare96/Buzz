"""OpenAI speech-to-text adapter for Buzz."""

from __future__ import annotations

import os
from pathlib import Path

from buzz.voice.speech_to_text import SpeechToText, Transcript


class OpenAISpeechToText(SpeechToText):
    def __init__(self, model: str | None = None) -> None:
        from openai import OpenAI

        self.model = model or os.getenv("BUZZ_STT_MODEL", "gpt-4o-transcribe")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def transcribe(self, audio_path: Path) -> Transcript:
        with audio_path.open("rb") as audio:
            result = self.client.audio.transcriptions.create(model=self.model, file=audio)
        return Transcript(text=result.text)
