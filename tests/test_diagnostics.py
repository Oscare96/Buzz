from buzz.config.settings import Settings
from buzz.diagnostics import self_check

def test_self_check_requires_openai_for_core_test(tmp_path,monkeypatch):
    monkeypatch.setenv("BUZZ_WORKSPACE",str(tmp_path/"workspace"))
    report=self_check(Settings("","",""))
    assert report["ready_for_core_test"] is False
    assert any(c["name"]=="workspace" and c["ok"] for c in report["checks"])

def test_self_check_ready_with_openai_key(tmp_path,monkeypatch):
    monkeypatch.setenv("BUZZ_WORKSPACE",str(tmp_path/"workspace"))
    report=self_check(Settings("key","",""))
    assert report["ready_for_core_test"] is True
