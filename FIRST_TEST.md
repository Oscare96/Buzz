# Buzz Core v0.1 — First PC Test

Do not place secrets in GitHub. Create a local `.env` from `.env.example`.

## Setup

On Windows PowerShell:

```powershell
git clone https://github.com/Oscare96/Buzz.git
cd Buzz
git checkout develop
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-core.txt
copy .env.example .env
```

Add `OPENAI_API_KEY` to the local `.env`, then run:

```powershell
python main.py
```

## First checks

Try these in order:

1. `Tell me my system information.`
2. `Open https://github.com/Oscare96/Buzz`
3. `Open Notepad.`

The first two exercise read/low-risk execution. Application launch is restricted to Buzz's approved application catalog. Sensitive commands are designed to stop for confirmation before execution.

Audit records are written locally under `.cache/buzz/audit.jsonl`.
