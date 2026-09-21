from buzz.security.approvals import ApprovalStore


def test_approval_is_single_use():
    store = ApprovalStore()
    approval = store.issue("danger", ttl_seconds=10)
    assert store.consume(approval.token, "danger")
    assert not store.consume(approval.token, "danger")


def test_approval_is_bound_to_skill():
    store = ApprovalStore()
    approval = store.issue("one", ttl_seconds=10)
    assert not store.consume(approval.token, "two")
