import json
from buzz.security.audit_log import AuditLog

def test_read_recent_skips_bad_lines_and_limits(tmp_path):
    path=tmp_path/"audit.jsonl"
    path.write_text('bad\n'+json.dumps({"a":1})+'\n'+json.dumps({"a":2})+'\n',encoding="utf-8")
    events=AuditLog(path).read_recent(2)
    assert events==[{"a":1},{"a":2}]
