Set-StrictMode -Version Latest
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PSScriptRoot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
if (Test-Path requirements.txt) {
  if ((Get-Content requirements.txt | Measure-Object -Line).Lines -gt 0) {
    pip install -r requirements.txt
  }
}
python run.py
