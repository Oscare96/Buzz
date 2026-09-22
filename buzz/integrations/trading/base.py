"""Provider-neutral contracts for existing trading systems."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TradingProvider(ABC):
    @abstractmethod
    def portfolio(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def bot_status(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def preview_order(self, symbol: str, side: str, quantity: float) -> dict[str, Any]:
        """Return an order preview without submitting it."""
        raise NotImplementedError

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, idempotency_key: str) -> dict[str, Any]:
        """Submit a previously authorized order and return broker confirmation."""
        raise NotImplementedError

    @abstractmethod
    def set_bot_enabled(self, bot: str, enabled: bool) -> dict[str, Any]:
        """Pause or resume an existing trading bot."""
        raise NotImplementedError
