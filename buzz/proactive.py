"""Composition helpers for Buzz proactive monitoring."""
from __future__ import annotations
from buzz.events.bus import EventBus
from buzz.events.monitor import PipelineMonitor
from buzz.events.proposals import PipelineFailureProposalHandler,ProposalStore
from buzz.integrations.devops.base import DevOpsProvider

class ProactiveService:
    def __init__(self,devops:DevOpsProvider)->None:
        self.bus=EventBus()
        self.proposals=ProposalStore()
        self.bus.subscribe("devops.pipeline_failed",PipelineFailureProposalHandler(self.proposals))
        self.pipeline=PipelineMonitor(devops,self.bus)

    def check_pipeline(self,repository:str)->dict:
        status=self.pipeline.check(repository)
        return {
            "status":status,
            "proposals":[{
                "proposal_id":p.proposal_id,
                "title":p.title,
                "skill":p.skill,
                "arguments":p.arguments,
                "reason":p.reason,
                "source_event_id":p.source_event_id,
                "created_at":p.created_at,
            } for p in self.proposals.list()],
        }
