from buzz.voice.session import VoiceSession

def test_voice_session_can_be_deactivated():
    session=VoiceSession(); session.activate(); assert session.active
    session.deactivate(); assert not session.active
    assert session.expired()
