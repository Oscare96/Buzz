$ErrorActionPreference = "Stop"

Write-Host "Buzz Windows setup"
if (-not (Test-Path ".venv")) {
    py -m venv .venv
}
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-core.txt
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Add OPENAI_API_KEY before the full core test."
} else {
    Write-Host ".env already exists; leaving it unchanged."
}
python main.py --status
Write-Host "Setup complete. After adding OPENAI_API_KEY, run: python main.py --self-check"
