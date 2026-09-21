"""One-turn voice interaction loop for Buzz."""

from __future__ import annotations

from pathlib import Path
import tempfile

from buzz.core.request import BuzzRequest
from buzz.core.runtime import BuzzRuntime
from buzz.voice.recorder import record_wav
from buzz.voice.speech_to_text import SpeechToText
from buzz.voice.text_to_speech import TextToSpeech


class VoiceLoop:
    def __init__(self, runtime: BuzzRuntime, stt: SpeechToText, tts: TextToSpeech) -> None:
        self.runtime = runtime
        self.stt = stt
        self.tts = tts

    def listen_once(self, seconds: float = 6.0) -> str:
        with tempfile.TemporaryDirectory(prefix="buzz-") as temp:
            audio = record_wav(Path(temp) / "utterance.wav", seconds=seconds)
            transcript = self.stt.transcribe(audio)
        text = transcript.text.strip()
        if not text:
            return ""
        response = self.runtime.handle(BuzzRequest(text=text, source="voice"))
        if response.text:
            self.tts.speak(response.text)
        return response.text
