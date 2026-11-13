Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " AegisCode: AI Predictive Intelligence & Automated Program Repair" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Launching platform on http://localhost:8000 ..." -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot
python run.py

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Python was not found in PATH or exited with an error. Opening index.html directly..."
    Start-Process "$PSScriptRoot\index.html"
}
