import sys,types
from buzz.voice.openai_stt import OpenAISpeechToText

class Transcriptions:
    def __init__(self): self.kwargs=None
    def create(self,**kwargs): self.kwargs=kwargs; return types.SimpleNamespace(text="hello buzz")
class Client:
    def __init__(self): self.audio=types.SimpleNamespace(transcriptions=Transcriptions())

def test_stt_sends_audio_file_and_model(monkeypatch,tmp_path):
    client=Client()
    monkeypatch.setitem(sys.modules,"openai",types.SimpleNamespace(OpenAI=lambda **kwargs:client))
    monkeypatch.setenv("OPENAI_API_KEY","test")
    path=tmp_path/"audio.wav"; path.write_bytes(b"RIFFtest")
    stt=OpenAISpeechToText(model="test-stt")
    result=stt.transcribe(path)
    assert result.text=="hello buzz"
    assert client.audio.transcriptions.kwargs["model"]=="test-stt"
