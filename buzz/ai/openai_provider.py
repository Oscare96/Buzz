"""OpenAI implementation of the Buzz AI provider."""

from __future__ import annotations

import os

from buzz.ai.provider import AIProvider, AIResponse


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        from openai import OpenAI

        self.model = model or os.getenv("BUZZ_OPENAI_MODEL", "gpt-5.6")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def respond(self, message: str) -> AIResponse:
        response = self.client.responses.create(model=self.model, input=message)
        return AIResponse(text=response.output_text, provider=self.name, model=self.model)
