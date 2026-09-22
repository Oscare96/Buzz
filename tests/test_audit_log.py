import json

from buzz.security.audit import AuditEvent
from buzz.security.audit_log import AuditLog


def test_audit_log_appends_json(tmp_path):
    path = tmp_path / "audit.jsonl"
    AuditLog(path).write(AuditEvent("system.info", "success"))
    record = json.loads(path.read_text(encoding="utf-8").strip())
    assert record["action"] == "system.info"
    assert record["outcome"] == "success"
    assert record["timestamp"]
