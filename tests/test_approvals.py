from buzz.security.approvals import ApprovalStore


def test_approval_is_single_use():
    store = ApprovalStore()
    args = {"target": "demo"}
    approval = store.issue("danger", args, ttl_seconds=10)
    assert store.consume(approval.token, "danger", args)
    assert not store.consume(approval.token, "danger", args)


def test_approval_is_bound_to_exact_action():
    store = ApprovalStore()
    approval = store.issue("one", {"target": "a"}, ttl_seconds=10)
    assert not store.consume(approval.token, "one", {"target": "b"})
