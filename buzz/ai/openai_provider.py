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
        response = self.client.responses.create(
            model=self.model,
            input=message,
            text={"format": {"type": "json_schema", "name": "buzz_plan", "strict": True, "schema": {
                "type": "object",
                "properties": {
                    "reply": {"type": "string"},
                    "actions": {"type": "array", "items": {"type": "object", "properties": {
                        "skill": {"type": "string"}, "arguments": {"type": "object"}, "reason": {"type": "string"}
                    }, "required": ["skill", "arguments", "reason"], "additionalProperties": False}}
                },
                "required": ["reply", "actions"], "additionalProperties": False
            }}},
        )
        return AIResponse(text=response.output_text, provider=self.name, model=self.model)
