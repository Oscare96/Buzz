from buzz.config.settings import Settings
from buzz.skills.defaults import build_default_registry

def test_trading_disabled_without_credentials():
    settings=Settings("key","","")
    names=build_default_registry(settings).names()
    assert "trading.portfolio" not in names
    assert "trading.place_order" not in names
