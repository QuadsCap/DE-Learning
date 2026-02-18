# run_pipeline.ps1
# Purpose:
# - One-command pipeline runner for DE-Learning
# - Activates venv, runs ingest, then runs verify
# - Stops immediately if any step fails

$ErrorActionPreference = "Stop"

Write-Host "=== DE-Learning: Run Pipeline ==="

# 1) Move to repo root (folder where this script lives)
Set-Location $PSScriptRoot

# 2) Activate virtual environment
if (!(Test-Path ".\.venv\Scripts\Activate.ps1")) {
    throw "Virtual environment not found. Create it with: python -m venv .venv"
}

Write-Host "Activating venv..."
. .\.venv\Scripts\Activate.ps1

# 3) Run ingestion
Write-Host "`nRunning ingestion..."
python .\src\python\ingest_prices.py

# 4) Run verification
Write-Host "`nRunning verification..."
python .\src\python\verify_prices.py

Write-Host "`nOK: Pipeline completed."
