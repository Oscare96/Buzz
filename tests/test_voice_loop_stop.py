from pathlib import Path
from buzz.ai.provider import AIProvider,AIResponse
from buzz.core.router import ToolRouter
from buzz.core.runtime import BuzzRuntime
from buzz.skills.registry import SkillRegistry
from buzz.voice.session import VoiceSession
from buzz.voice.speech_to_text import SpeechToText,Transcript
from buzz.voice.text_to_speech import TextToSpeech
from buzz.voice.voice_loop import VoiceLoop

class Planner(AIProvider):
    def respond(self,message): return AIResponse('{"reply":"ok","actions":[]}',"test")
class STT(SpeechToText):
    def transcribe(self,path:Path): return Transcript("Buzz stop")
class TTS(TextToSpeech):
    def __init__(self): self.stopped=False; self.spoken=[]
    def speak(self,text): self.spoken.append(text)
    def stop(self): self.stopped=True

def test_spoken_stop_deactivates_session(monkeypatch,tmp_path):
    import sys,types
    fake=types.ModuleType("buzz.voice.recorder")
    fake.record_wav=lambda path,seconds:path
    monkeypatch.setitem(sys.modules,"buzz.voice.recorder",fake)
    session=VoiceSession(); session.activate(); tts=TTS()
    loop=VoiceLoop(BuzzRuntime(Planner(),ToolRouter(SkillRegistry())),STT(),tts,session)
    assert loop.listen_once(0.01)==""
    assert session.active is False
    assert tts.stopped is True
    assert tts.spoken==[]
