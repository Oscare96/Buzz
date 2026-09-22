"""ElevenLabs text-to-speech adapter for Buzz."""

from __future__ import annotations

import os
import threading

import numpy as np
import sounddevice as sd

from buzz.voice.text_to_speech import TextToSpeech


class ElevenLabsTTS(TextToSpeech):
    def __init__(self) -> None:
        from elevenlabs.client import ElevenLabs

        api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
        if not api_key or not self.voice_id:
            raise RuntimeError("ElevenLabs API key and voice ID are required.")
        self.client = ElevenLabs(api_key=api_key)
        self.model = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.sample_rate = 24000
        self._lock = threading.Lock()

    def speak(self, text: str) -> None:
        chunks = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            text=text,
            model_id=self.model,
            output_format="pcm_24000",
        )
        raw = b"".join(chunks)
        if not raw:
            return
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        with self._lock:
            sd.play(audio, self.sample_rate)
            sd.wait()

    def stop(self) -> None:
        sd.stop()
