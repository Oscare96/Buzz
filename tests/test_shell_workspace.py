import os
from buzz.skills.shell import ShellCommandSkill

def test_shell_rejects_cwd_outside_workspace(tmp_path, monkeypatch):
    workspace=tmp_path/"workspace"; outside=tmp_path/"outside"
    monkeypatch.setenv("BUZZ_WORKSPACE",str(workspace))
    result=ShellCommandSkill().execute(argv=["python","--version"],cwd=str(outside))
    assert not result.success
    assert "inside Buzz workspace" in result.message
