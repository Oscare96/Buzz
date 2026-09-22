"""Voice interaction loop for Buzz with short continuous sessions."""
from __future__ import annotations
from pathlib import Path
import tempfile
from buzz.core.request import BuzzRequest
from buzz.core.runtime import BuzzRuntime
from buzz.voice.session import VoiceSession
from buzz.voice.speech_to_text import SpeechToText
from buzz.voice.text_to_speech import TextToSpeech

class VoiceLoop:
    def __init__(self,runtime:BuzzRuntime,stt:SpeechToText,tts:TextToSpeech,session:VoiceSession|None=None)->None:
        self.runtime=runtime; self.stt=stt; self.tts=tts; self.session=session or VoiceSession()
    def listen_once(self,seconds:float=6.0)->str:
        from buzz.voice.recorder import record_wav
        with tempfile.TemporaryDirectory(prefix="buzz-") as temp:
            audio=record_wav(Path(temp)/"utterance.wav",seconds=seconds); transcript=self.stt.transcribe(audio)
        text=transcript.text.strip()
        if not text:return ""
        if text.lower() in {"buzz stop","stop buzz","stop listening","goodbye buzz"}:
            self.tts.stop(); self.session.deactivate(); return ""
        self.session.activate() if not self.session.active else self.session.touch()
        response=self.runtime.handle(BuzzRequest(text=text,source="voice"))
        if response.text:self.tts.speak(response.text)
        return response.text
    def conversation(self,seconds:float=6.0,max_turns:int=8,max_silence_turns:int=2)->None:
        self.session.activate()
        turns=0; silence_turns=0
        while self.session.active and not self.session.expired() and turns<max_turns:
            response=self.listen_once(seconds=seconds); turns+=1
            if not self.session.active: break
            if response:
                silence_turns=0
            else:
                silence_turns+=1
                if silence_turns>=max_silence_turns:
                    self.session.deactivate()
                    break
