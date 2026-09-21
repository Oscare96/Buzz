import sys
from buzz.skills.shell import ShellCommandSkill


def test_shell_skill_uses_argv_and_returns_output():
    result = ShellCommandSkill().execute(argv=[sys.executable, "-c", "print('buzz')"])
    assert result.success
    assert result.data["stdout"].strip() == "buzz"
