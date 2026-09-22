from buzz.config.settings import Settings
from buzz.status import status_report

def test_voice_ready_requires_wake_model_and_cloud_voice_credentials():
    incomplete=Settings("openai","eleven","voice")
    assert status_report(incomplete)["voice_configured"] is False
    ready=Settings("openai","eleven","voice",wake_model="hey_buzz.onnx")
    report=status_report(ready)
    assert report["voice_configured"] is True
    assert report["wake_model_configured"] is True
