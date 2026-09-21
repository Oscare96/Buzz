"""openWakeWord adapter for local Buzz wake-word detection."""

from __future__ import annotations

import os

import numpy as np
import sounddevice as sd

from buzz.voice.wake_word import WakeWordDetector


class OpenWakeWordDetector(WakeWordDetector):
    def __init__(self, model_path: str | None = None, threshold: float = 0.5) -> None:
        from openwakeword.model import Model

        model_path = model_path or os.getenv("BUZZ_WAKE_MODEL", "").strip()
        if not model_path:
            raise RuntimeError("BUZZ_WAKE_MODEL must point to an openWakeWord model file.")
        self.model = Model(wakeword_models=[model_path])
        self.threshold = threshold
        self._stream = None
        self._detected = False

    def _callback(self, indata, frames, time_info, status) -> None:
        del frames, time_info, status
        audio = (indata[:, 0] * 32767).astype(np.int16)
        scores = self.model.predict(audio)
        if scores and max(float(value) for value in scores.values()) >= self.threshold:
            self._detected = True

    def start(self) -> None:
        self._detected = False
        self._stream = sd.InputStream(samplerate=16000, channels=1, dtype="float32", blocksize=1280, callback=self._callback)
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def detected(self) -> bool:
        if self._detected:
            self._detected = False
            return True
        return False
