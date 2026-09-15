@echo off
setlocal
cd /d "%~dp0"
title System 64 - ChatBot Desktop Agent

echo ========================================
echo       SYSTEM 64 - STARTING UP
echo ========================================
echo.

echo [1/3] Starting Desktop Agent...
start "System 64 Desktop Agent" /min cmd /k "python desktop_agent.py"

timeout /t 2 /nobreak >nul

echo [2/3] Starting ChatBot web interface...
start "System 64 ChatBot" /min cmd /k "python app.py"

timeout /t 3 /nobreak >nul

echo [3/3] Starting wake-word listener...
start "System 64 Wake Word" /min cmd /k "python wake_word.py"

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:5000"
echo.
echo System 64 is running.
echo Say: "System 64, wake up"
echo.
pause
