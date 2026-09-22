"""Microphone recording utility for a single Buzz utterance."""

from __future__ import annotations

from pathlib import Path
import wave

import numpy as np
import sounddevice as sd


def record_wav(path: Path, seconds: float = 6.0, sample_rate: int = 16000) -> Path:
    if seconds <= 0:
        raise ValueError("Recording duration must be positive.")
    frames = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(np.dtype(np.int16).itemsize)
        wav.setframerate(sample_rate)
        wav.writeframes(frames.tobytes())
    return path
