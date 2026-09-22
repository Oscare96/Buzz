from buzz.config.settings import Settings
from buzz.skills.defaults import build_default_registry

def test_trading_disabled_without_credentials():
    settings=Settings("key","","")
    names=build_default_registry(settings).names()
    assert "trading.portfolio" not in names
    assert "trading.place_order" not in names


def test_paper_credentials_enable_execution_skill():
    settings=Settings("key","","",alpaca_api_key="paper-key",alpaca_secret_key="paper-secret")
    names=build_default_registry(settings).names()
    assert "trading.portfolio" in names
    assert "trading.preview_order" in names
    assert "trading.place_order" in names

def test_non_paper_endpoint_does_not_enable_execution_skill():
    settings=Settings("key","","",alpaca_api_key="key",alpaca_secret_key="secret",alpaca_base_url="https://api.alpaca.markets")
    names=build_default_registry(settings).names()
    assert "trading.portfolio" in names
    assert "trading.preview_order" in names
    assert "trading.place_order" not in names
