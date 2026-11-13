@echo off
title Push QuickFix to GitHub
cls
cd /d "%~dp0"

echo ======================================================================
echo  Pushing QuickFix to https://github.com/mohammad-sameer441/QuickFix.git
echo ======================================================================
echo.

git init
git remote remove origin 2>nul
git remote add origin https://github.com/mohammad-sameer441/QuickFix.git
git branch -M main
git add .
git commit -m "feat: initial commit of QuickFix AI-driven program repair platform"

echo.
echo Pushing to GitHub (main branch)...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [✔] SUCCESS! Project pushed to:
    echo     https://github.com/mohammad-sameer441/QuickFix
    echo ======================================================================
) else (
    echo.
    echo [!] If authentication is required, GitHub will prompt for your credentials
    echo     or Personal Access Token (PAT).
    echo [!] If the remote repo already has a README or commit, run:
    echo     git pull origin main --allow-unrelated-histories --no-rebase
    echo     git push -u origin main
)

echo.
pause
