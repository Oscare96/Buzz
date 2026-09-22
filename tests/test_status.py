from buzz.config.settings import Settings
from buzz.status import status_report

def test_status_works_without_ai_credentials():
    report=status_report(Settings("","",""))
    assert report["ai_configured"] is False
    assert "system.info" in report["skills"]
    assert report["alpaca_paper_execution"] is False
