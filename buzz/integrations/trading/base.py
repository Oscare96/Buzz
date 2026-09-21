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
