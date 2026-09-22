"""Central request lifecycle for Buzz.

The orchestrator will coordinate AI providers, tools, permissions, execution,
verification, and reporting. Keeping this layer provider-independent prevents
Buzz from being tied to one AI vendor.
"""

from dataclasses import dataclass
from enum import Enum


class BuzzState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    ACTING = "acting"
    SPEAKING = "speaking"


@dataclass
class BuzzOrchestrator:
    state: BuzzState = BuzzState.IDLE

    def set_state(self, state: BuzzState) -> None:
        self.state = state
