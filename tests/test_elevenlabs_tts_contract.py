import sys,types
import numpy as np

class TTSAPI:
    def __init__(self): self.kwargs=None
    def convert(self,**kwargs): self.kwargs=kwargs; return [b"\x00\x00\x01\x00"]
class Client:
    def __init__(self,**kwargs): self.text_to_speech=TTSAPI()

def test_elevenlabs_pcm_contract(monkeypatch):
    client=Client()
    monkeypatch.setitem(sys.modules,"elevenlabs",types.ModuleType("elevenlabs"))
    mod=types.ModuleType("elevenlabs.client"); mod.ElevenLabs=lambda **kwargs:client
    monkeypatch.setitem(sys.modules,"elevenlabs.client",mod)
    monkeypatch.setenv("ELEVENLABS_API_KEY","test"); monkeypatch.setenv("ELEVENLABS_VOICE_ID","voice")
    import buzz.voice.elevenlabs_tts as module
    played=[]
    monkeypatch.setattr(module.sd,"play",lambda audio,rate:played.append((audio,rate)))
    monkeypatch.setattr(module.sd,"wait",lambda:None)
    tts=module.ElevenLabsTTS(); tts.speak("hello")
    assert client.text_to_speech.kwargs["output_format"]=="pcm_24000"
    assert played and played[0][1]==24000 and played[0][0].dtype==np.float32
