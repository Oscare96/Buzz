# Buzz Voice — Windows Integration Test

Run this only after the core PC test passes.

## Install the voice stack

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-voice.txt
```

In the local `.env`, configure:

- `OPENAI_API_KEY`
- `BUZZ_STT_MODEL=gpt-4o-transcribe`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `BUZZ_WAKE_MODEL` with the local openWakeWord model path/name used for Buzz

Never commit the populated `.env`.

## Readiness

```powershell
.\.venv\Scripts\python.exe main.py --status
```

Do not start the live test until `voice_configured` is true.

## Live test

```powershell
.\.venv\Scripts\python.exe main.py --voice
```

Test in this order: wake Buzz, ask a harmless information question, ask Buzz to open Notepad, continue with a second utterance without re-waking during the active session, then say `Buzz stop`.

This is the first hardware/API integration test. If microphone selection, PortAudio, wake-word loading, transcription, or ElevenLabs playback fails, capture the exact terminal output before changing configuration.
