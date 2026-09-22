#!/usr/bin/env python3
"""Buzz application entry point."""
import argparse
import json
from buzz.cli import run_cli
from buzz.status import status_report

def main() -> int:
    parser=argparse.ArgumentParser(description="Buzz personal AI automation platform")
    parser.add_argument("--status",action="store_true",help="show local configuration and enabled capabilities without starting AI")
    parser.add_argument("--api",action="store_true",help="start the local Buzz API on 127.0.0.1")
    parser.add_argument("--voice",action="store_true",help="start wake-word-driven Buzz voice mode")
    args=parser.parse_args()
    if args.status:
        print(json.dumps(status_report(),indent=2))
        return 0
    if args.voice:
        from buzz.app import build_runtime
        from buzz.voice.assistant import VoiceAssistant
        from buzz.voice.elevenlabs_tts import ElevenLabsTTS
        from buzz.voice.openai_stt import OpenAISpeechToText
        from buzz.voice.openwakeword_detector import OpenWakeWordDetector
        from buzz.voice.voice_loop import VoiceLoop
        VoiceAssistant(OpenWakeWordDetector(),VoiceLoop(build_runtime(),OpenAISpeechToText(),ElevenLabsTTS())).run()
        return 0
    if args.api:
        try:
            import uvicorn
        except ImportError as exc:
            raise SystemExit("Install requirements-api.txt before using --api.") from exc
        uvicorn.run("buzz.api:app",host="127.0.0.1",port=8765,reload=False)
        return 0
    return run_cli()

if __name__=="__main__":
    raise SystemExit(main())
