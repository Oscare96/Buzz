from buzz.events.models import BuzzEvent
from buzz.events.proposals import PipelineFailureProposalHandler,ProposalStore

def test_failed_pipeline_creates_rerun_proposal_only():
    store=ProposalStore(); handler=PipelineFailureProposalHandler(store)
    event=BuzzEvent(kind="devops.pipeline_failed",source="github",payload={
        "repository":"Oscare96/Buzz",
        "status":{"path":".github/workflows/ci.yml","head_branch":"develop"},
    })
    handler(event)
    proposals=store.list()
    assert len(proposals)==1
    proposal=proposals[0]
    assert proposal.skill=="devops.run_pipeline"
    assert proposal.arguments["ref"]=="develop"
    assert proposal.source_event_id==event.event_id

def test_incomplete_event_does_not_create_executable_proposal():
    store=ProposalStore(); PipelineFailureProposalHandler(store)(BuzzEvent(kind="devops.pipeline_failed",source="github",payload={"repository":"Oscare96/Buzz","status":{}}))
    assert store.list()==()
