import sys,types
from buzz.config.settings import Settings
from buzz.voice.diagnostics import voice_check

def test_voice_check_reports_missing_config_without_hardware(monkeypatch):
    fake=types.ModuleType("sounddevice")
    fake.query_devices=lambda: []
    fake.default=types.SimpleNamespace(device=(-1,-1))
    monkeypatch.setitem(sys.modules,"sounddevice",fake)
    report=voice_check(Settings("","",""))
    assert report["ready_for_voice_test"] is False
    names={c["name"] for c in report["checks"]}
    assert {"openai_key","elevenlabs_key","elevenlabs_voice","wake_model","microphone"}<=names

def test_voice_check_can_pass_with_mocked_microphone(monkeypatch,tmp_path):
    model=tmp_path/"buzz.onnx"; model.write_bytes(b"model")
    fake=types.ModuleType("sounddevice")
    fake.query_devices=lambda: [{"name":"Test Mic","max_input_channels":1}]
    fake.default=types.SimpleNamespace(device=(0,0))
    monkeypatch.setitem(sys.modules,"sounddevice",fake)
    settings=Settings("openai","eleven","voice",wake_model=str(model))
    report=voice_check(settings)
    assert report["ready_for_voice_test"] is True
