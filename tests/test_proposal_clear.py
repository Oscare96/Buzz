from buzz.events.proposals import ActionProposal,ProposalStore

def test_proposal_store_can_clear_resolved_state():
    store=ProposalStore(); store.add(ActionProposal("x","system.info",{},"r","e"))
    store.clear()
    assert store.list()==()
