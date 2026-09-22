from buzz.security.audit import AuditEvent
from buzz.security.audit_log import AuditLog

def test_audit_redacts_bearer_tokens(tmp_path):
    log=AuditLog(tmp_path/"audit.jsonl")
    log.write(AuditEvent("test","blocked","Authorization=Bearer abcdefghijklmnopqrstuvwxyz"))
    raw=(tmp_path/"audit.jsonl").read_text(encoding="utf-8")
    assert "abcdefghijklmnopqrstuvwxyz" not in raw
    assert "REDACTED" in raw
