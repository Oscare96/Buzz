from buzz.config.settings import Settings
from buzz.status import status_report

def test_status_reports_api_control_token():
    assert status_report(Settings("","",""))["api_control_configured"] is False
    assert status_report(Settings("","","",api_token="token"))["api_control_configured"] is True
