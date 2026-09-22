from buzz import api

class FakeApprovals:
    def pending_count(self): return 3
class FakeRuntime:
    approvals=FakeApprovals()

def test_pending_approval_endpoint_exposes_count_not_tokens(monkeypatch):
    monkeypatch.setattr(api,"runtime",lambda:FakeRuntime())
    result=api.pending_approvals()
    assert result=={"count":3}
    assert "token" not in result
