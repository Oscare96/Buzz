from buzz.skills.computer import OpenApplicationSkill, OpenUrlSkill


def test_unknown_application_is_blocked():
    result = OpenApplicationSkill().execute(app="made-up-app")
    assert not result.success


def test_non_http_url_is_blocked():
    result = OpenUrlSkill().execute(url="file:///tmp/example")
    assert not result.success
