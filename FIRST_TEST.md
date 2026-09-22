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

Before adding any cloud credentials, verify that Buzz boots and reports its local capability state:

```powershell
python main.py --status
```

This status command does not require an OpenAI key. It should report the core local skills and show optional integrations as disabled until their credentials are configured.

Then add `OPENAI_API_KEY` to the local `.env` and run the readiness check:

```powershell
python main.py --self-check
```

When `ready_for_core_test` is `true`, start Buzz:

```powershell
python main.py
```

## First checks

Try these in order:

1. `Tell me my system information.`
2. `Open https://github.com/Oscare96/Buzz`
3. `Open Notepad.`
4. `Create a file named first-test.txt in my Buzz workspace containing Buzz is working.` Confirm the action when Buzz asks.
5. `Run the command python --version.` Confirm the action when Buzz asks.

The first three exercise read/low-risk execution. The last two verify that Buzz can perform an authorized system-changing action itself rather than only explaining what to do. Application launch is restricted to Buzz's approved application catalog. Sensitive commands are designed to stop for confirmation before execution.

Audit records are written locally under `.cache/buzz/audit.jsonl`.
