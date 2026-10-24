@echo off
REM ==============================================================================
REM PNN Discovery Pipeline - Turnkey One-Click Launcher (Windows)
REM ==============================================================================
title PNN Discovery Pipeline

echo [PNN] Starting PNN Perineuronal Net Drug Discovery Pipeline...
python run.py --no-browser %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Pipeline encountered an error (exit code: %ERRORLEVEL%).
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [PNN] Turnkey execution succeeded! Dashboard generated at studio.html
pause
