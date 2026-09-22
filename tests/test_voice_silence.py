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
    def respond(self,message): return AIResponse('{"reply":"","actions":[]}',"test")
class SilentSTT(SpeechToText):
    def transcribe(self,path:Path): return Transcript("")
class TTS(TextToSpeech):
    def speak(self,text): pass
    def stop(self): pass

def test_repeated_silence_ends_conversation(monkeypatch):
    monkeypatch.setattr("buzz.voice.voice_loop.record_wav",lambda path,seconds:path)
    session=VoiceSession(timeout_seconds=60)
    loop=VoiceLoop(BuzzRuntime(Planner(),ToolRouter(SkillRegistry())),SilentSTT(),TTS(),session)
    loop.conversation(seconds=.01,max_turns=8,max_silence_turns=2)
    assert session.active is False
