# Buzz

Buzz is a modular personal AI automation platform being built from the original Jarvis-style desktop clap project.

## Current architecture

Buzz separates AI reasoning from trusted execution. Requests flow through the core orchestrator, provider-neutral AI adapters, a permission-aware tool router, registered skills, verification, and audit/reporting layers.

Core packages currently include:

- `buzz/core` — orchestration, requests, and tool routing
- `buzz/ai` — replaceable AI providers; OpenAI adapter included
- `buzz/voice` — wake word, STT, TTS, and conversation sessions
- `buzz/skills` — trusted capabilities such as computer control
- `buzz/security` — risk levels, authorization, and audit models
- `buzz/events` — proactive event model and event bus
- `buzz/memory` — memory abstraction separated from secrets/operational state

The original `jarvis.py` remains available during migration as the baseline implementation.

## Security model

Actions are classified from read-only through critical. System-changing and critical actions require confirmation before the tool router executes them. Secrets belong in a local `.env` file and are excluded from Git.

## Development setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
copy .env.example .env
pytest
python main.py
```

Populate the required provider keys in `.env` before enabling cloud AI or ElevenLabs voice.

For the first Windows test, run `scripts/setup_windows.ps1`, add `OPENAI_API_KEY` to the local `.env`, then run `python main.py --self-check`. The full checklist is in `FIRST_TEST.md`.

### Local API

Buzz also has a localhost-only API foundation for future desktop and mobile clients:

```bash
pip install -r requirements-api.txt
python main.py --api
```

It binds to `127.0.0.1:8765` by default. Set `BUZZ_API_TOKEN` in `.env` to require a bearer token for control endpoints. The API includes health, status, request, approval, and recent audit endpoints. Do not expose it directly to the public internet. Remote/mobile access will be added behind authenticated secure transport.

### Proactive pipeline check

With a least-privilege `BUZZ_GITHUB_TOKEN` configured, Buzz can inspect a repository's latest GitHub Actions run without changing anything:

```bash
python main.py --check-pipeline Oscare96/Buzz
```

If a failed run contains an exact workflow path and branch, Buzz can produce a rerun proposal. It does not execute the rerun automatically; the normal authorization and confirmation path still applies.

## Branches

`main` preserves the fork baseline while active Buzz development happens on `develop`.

## Origin

Buzz began as a fork of Hector G.'s Jarvis desktop automation project at https://github.com/hectorg2211/jarvis. The original `jarvis.py` is retained during the migration while Buzz evolves into a modular execution-first assistant.
