from buzz.api import dashboard

def test_dashboard_page_contains_buzz_control_center():
    page=dashboard()
    assert "Buzz Control Center" in page
    assert "Port 8787" in page\n    assert "Talk to Buzz" in page\n    assert 'fetch("/request"' in page
