from buzz.security.approvals import ApprovalStore

def test_pending_count_tracks_issue_and_consume():
    store=ApprovalStore(); approval=store.issue("x",{"a":1})
    assert store.pending_count()==1
    assert store.consume(approval.token,"x",{"a":1}) is True
    assert store.pending_count()==0

def test_pending_count_removes_expired():
    store=ApprovalStore(); store.issue("x",{},ttl_seconds=-1)
    assert store.pending_count()==0
