"""Home Assistant REST integration for Buzz."""

from __future__ import annotations

from typing import Any
import requests
from buzz.integrations.home.base import HomeProvider


class HomeAssistantProvider(HomeProvider):
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def state(self, entity_id: str) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/api/states/{entity_id}", headers=self.headers, timeout=15)
        response.raise_for_status()
        return response.json()

    def call_service(self, domain: str, service: str, entity_id: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(data or {})
        payload["entity_id"] = entity_id
        response = requests.post(f"{self.base_url}/api/services/{domain}/{service}", headers=self.headers, json=payload, timeout=15)
        response.raise_for_status()
        return {"result": response.json()}
