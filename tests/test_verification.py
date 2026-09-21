from buzz.core.verification import verify_success
from buzz.skills.base import SkillResult

def test_verify_success():
    result = verify_success(SkillResult(True, "ok", {"id": 1}))
    assert result.verified and result.data["id"] == 1
