Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " Pushing QuickFix to https://github.com/mohammad-sameer441/QuickFix.git" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

git init
git remote remove origin 2>$null
git remote add origin https://github.com/mohammad-sameer441/QuickFix.git
git branch -M main
git add .
git commit -m "feat: initial commit of QuickFix AI-driven program repair platform"

Write-Host "`nPushing to GitHub (main branch)..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[✔] SUCCESS! Project pushed to https://github.com/mohammad-sameer441/QuickFix" -ForegroundColor Green
} else {
    Write-Host "`n[!] Push requires authentication or existing remote files need sync." -ForegroundColor Red
    Write-Host "Run: git pull origin main --allow-unrelated-histories --no-rebase" -ForegroundColor Yellow
    Write-Host "Then: git push -u origin main" -ForegroundColor Yellow
}
