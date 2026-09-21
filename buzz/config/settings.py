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
    home_assistant_url: str = ""
    home_assistant_token: str = ""

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY","").strip(),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY","").strip(),
            elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID","").strip(),
            home_assistant_url=os.getenv("HOME_ASSISTANT_URL","").strip(),
            home_assistant_token=os.getenv("HOME_ASSISTANT_TOKEN","").strip(),
        )

    def validate_ai(self) -> None:
        if not self.openai_api_key: raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env.")

    @property
    def home_assistant_enabled(self) -> bool:
        return bool(self.home_assistant_url and self.home_assistant_token)
