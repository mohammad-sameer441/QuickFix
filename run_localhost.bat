@echo off
title QuickFix Localhost Platform
cls
echo ======================================================================
echo  QuickFix: AI Predictive Intelligence ^& Automated Program Repair
echo ======================================================================
echo.
echo Launching QuickFix on http://localhost:8000 ...
echo.

cd /d "%~dp0"
python run.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Python was not found in PATH or exited with an error.
    echo [*] Attempting to open index.html directly in your default browser...
    start "" "%~dp0index.html"
)

pause
