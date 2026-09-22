from buzz.events.proposals import ActionProposal,ProposalStore

def test_identical_source_action_is_not_duplicated():
    store=ProposalStore()
    a=ActionProposal("Rerun","devops.run_pipeline",{"repository":"a/b"},"failed","event-1")
    b=ActionProposal("Rerun","devops.run_pipeline",{"repository":"a/b"},"failed","event-1")
    store.add(a); store.add(b)
    assert len(store.list())==1
