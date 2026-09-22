from pathlib import Path
from buzz.ai.provider import AIProvider,AIResponse
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.security.audit_log import AuditLog
from buzz.skills.registry import SkillRegistry

class Planner(AIProvider):
    def respond(self,message): return AIResponse('{"reply":"ok","actions":[]}',"test")

def test_invalid_approval_is_audited(tmp_path:Path):
    log=AuditLog(tmp_path/"audit.jsonl")
    runtime=BuzzRuntime(Planner(),ToolRouter(SkillRegistry(),log))
    result=runtime.confirm("computer.run_command",{"argv":["echo","hi"]},"bad")
    assert result.success is False
    events=log.read_recent()
    assert events[-1]["outcome"]=="approval_rejected"
