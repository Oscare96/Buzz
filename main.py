#!/usr/bin/env python3
"""Buzz application entry point."""
import argparse
import json
from buzz.cli import run_cli
from buzz.status import status_report
from buzz.diagnostics import self_check

def main() -> int:
    parser=argparse.ArgumentParser(description="Buzz personal AI automation platform")
    parser.add_argument("--status",action="store_true",help="show local configuration and enabled capabilities without starting AI")
    parser.add_argument("--api",action="store_true",help="start the local Buzz API on 127.0.0.1")
    parser.add_argument("--voice",action="store_true",help="start wake-word-driven Buzz voice mode")
    parser.add_argument("--self-check",action="store_true",help="run local readiness checks before the first PC test")
    parser.add_argument("--check-pipeline",metavar="OWNER/REPO",help="check one GitHub pipeline and show any safe proactive proposal")
    parser.add_argument("--voice-check",action="store_true",help="check voice credentials, wake model, and microphone without starting Buzz")
    args=parser.parse_args()
    if args.status:
        print(json.dumps(status_report(),indent=2))
        return 0
    if args.self_check:
        report=self_check()
        print(json.dumps(report,indent=2))
        return 0 if report["ready_for_core_test"] else 1
    if args.voice_check:
        from buzz.voice.diagnostics import voice_check
        report=voice_check()
        print(json.dumps(report,indent=2))
        return 0 if report["ready_for_voice_test"] else 1
    if args.check_pipeline:
        from buzz.config.settings import Settings
        from buzz.integrations.devops.github import GitHubDevOpsProvider
        from buzz.proactive import ProactiveService
        settings=Settings.load()
        if not settings.github_enabled:
            raise SystemExit("BUZZ_GITHUB_TOKEN is missing. Add a least-privilege token to .env.")
        result=ProactiveService(GitHubDevOpsProvider(settings.github_token)).check_pipeline(args.check_pipeline)
        print(json.dumps(result,indent=2))
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
        uvicorn.run("buzz.api:app",host="127.0.0.1",port=8787,reload=False)
        return 0
    return run_cli()

if __name__=="__main__":
    raise SystemExit(main())
