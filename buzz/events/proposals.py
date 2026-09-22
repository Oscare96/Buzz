"""Proactive suggestions that never bypass Buzz authorization."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from datetime import datetime, timezone
import json
from buzz.events.models import BuzzEvent

@dataclass(frozen=True)
class ActionProposal:
    title: str
    skill: str
    arguments: dict[str,Any]
    reason: str
    source_event_id: str
    proposal_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProposalStore:
    def __init__(self)->None:
        self._items: dict[str,ActionProposal]={}
    def add(self,proposal:ActionProposal)->None:
        fingerprint=(proposal.skill,json.dumps(proposal.arguments,sort_keys=True,separators=(",",":"),default=str),proposal.source_event_id)
        for existing in self._items.values():
            if (existing.skill,json.dumps(existing.arguments,sort_keys=True,separators=(",",":"),default=str),existing.source_event_id)==fingerprint:
                return
        self._items[proposal.proposal_id]=proposal
    def list(self)->tuple[ActionProposal,...]:
        return tuple(self._items.values())
    def get(self,proposal_id:str)->ActionProposal|None:
        return self._items.get(proposal_id)
    def pop(self,proposal_id:str)->ActionProposal|None:
        return self._items.pop(proposal_id,None)
    def clear(self)->None:
        self._items.clear()

class PipelineFailureProposalHandler:
    """Suggest a rerun when GitHub supplies an exact workflow path/ref; never executes it."""
    def __init__(self,store:ProposalStore)->None:
        self.store=store
    def __call__(self,event:BuzzEvent)->None:
        status=event.payload.get("status",{})
        repository=str(event.payload.get("repository","")).strip()
        workflow=str(status.get("path") or "").strip()
        ref=str(status.get("head_branch") or "").strip()
        if not repository or not workflow or not ref:
            return
        self.store.add(ActionProposal(
            title="Rerun failed workflow",
            skill="devops.run_pipeline",
            arguments={"repository":repository,"workflow":workflow,"ref":ref},
            reason="The latest monitored GitHub Actions run failed.",
            source_event_id=event.event_id,
        ))
