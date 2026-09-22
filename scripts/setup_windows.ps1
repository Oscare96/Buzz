$ErrorActionPreference = "Stop"

Write-Host "Buzz Windows setup"
if (-not (Test-Path ".venv")) {
    py -m venv .venv
}
$Python = Join-Path $PWD ".venv\Scripts\python.exe"
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements-core.txt
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Add OPENAI_API_KEY before the full core test."
} else {
    Write-Host ".env already exists; leaving it unchanged."
}
& $Python main.py --status
Write-Host "Setup complete. After adding OPENAI_API_KEY, run: .\.venv\Scripts\python.exe main.py --self-check"
