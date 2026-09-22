#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-api.txt
.venv/bin/python main.py --init
.venv/bin/python main.py --status
printf '\nBuzz setup complete. Add OPENAI_API_KEY to .env, then run:\n  .venv/bin/python main.py --api\n'
