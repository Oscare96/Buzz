"""Environment-backed Buzz settings."""

from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", "").strip(),
            elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID", "").strip(),
        )

    def validate_ai(self) -> None:
        if not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env.")
