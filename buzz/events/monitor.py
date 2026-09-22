"""Proactive event monitors for Buzz."""
from __future__ import annotations
from buzz.events.bus import EventBus
from buzz.events.models import BuzzEvent
from buzz.integrations.devops.base import DevOpsProvider

class PipelineMonitor:
    def __init__(self, provider: DevOpsProvider, bus: EventBus) -> None:
        self.provider=provider; self.bus=bus; self._seen: dict[str, object]={}
    def check(self, repository: str) -> dict:
        status=self.provider.pipeline_status(repository)
        run_id=status.get("id")
        failed=status.get("conclusion")=="failure"
        if failed and run_id is not None and self._seen.get(repository)!=run_id:
            detail=self.provider.pipeline_failure(repository)
            self.bus.publish(BuzzEvent(kind="devops.pipeline_failed",source="github",payload={"repository":repository,"status":status,"failure":detail}))
            self._seen[repository]=run_id
        elif run_id is not None:
            self._seen[repository]=run_id
        return status
