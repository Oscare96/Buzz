from buzz.security.risk import RiskLevel
from buzz.skills.home import HomeAccessControlSkill, HomeServiceSkill

class FakeHome:
    def state(self, entity_id): return {"state":"off"}
    def call_service(self, domain, service, entity_id, data=None): return {"domain":domain,"service":service,"entity_id":entity_id}

def test_general_home_skill_blocks_access_control_domains():
    result = HomeServiceSkill(FakeHome()).execute(domain="lock",service="unlock",entity_id="lock.front")
    assert not result.success

def test_access_control_skill_is_critical():
    assert HomeAccessControlSkill(FakeHome()).risk_level == RiskLevel.CRITICAL
