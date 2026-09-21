from buzz.config.settings import Settings
from buzz.skills.defaults import build_default_registry

def test_optional_integrations_disabled_without_credentials():
    settings=Settings("key","","")
    names=build_default_registry(settings).names()
    assert "devops.pipeline_status" not in names
    assert "home.state" not in names
