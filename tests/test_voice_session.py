from buzz.voice.session import VoiceSession


def test_session_starts_inactive():
    session = VoiceSession()
    assert not session.active
    assert session.expired()


def test_session_can_activate_and_deactivate():
    session = VoiceSession()
    session.activate()
    assert session.active
    assert not session.expired()
    session.deactivate()
    assert session.expired()
