from buzz.api import dashboard

def test_dashboard_page_contains_buzz_control_center():
    page=dashboard()
    assert "Buzz Control Center" in page
    assert "Port 8787" in page
    assert "Talk to Buzz" in page
    assert 'fetch("/request"' in page
    assert 'fetch("/approve"' in page
    assert "Approval required:" in page
    assert "localStorage" not in page
    assert "sessionStorage" not in page
