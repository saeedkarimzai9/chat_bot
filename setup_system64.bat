@echo off
setlocal
cd /d "%~dp0"
title System 64 - Easy Setup

echo ========================================
echo        SYSTEM 64 - EASY SETUP
echo ========================================
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3.11+ first.
  pause
  exit /b 1
)

echo Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
  echo Ollama was not found. Install Ollama first.
  pause
  exit /b 1
)

echo.
echo Installing the project's Python packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Package installation failed. The window will stay open so you can read the error.
  pause
  exit /b 1
)

echo.
echo Checking for an installed Ollama model...
ollama list

echo.
echo System 64 is configured to use: qwen2.5-coder:7b
echo If qwen2.5-coder:7b appears above, the AI model is ready.
echo The wake-word listener also needs the Vosk English model at:
echo models\vosk-model-small-en-us
echo.
echo Setup finished.
echo Run system64_launcher.bat to start System 64.
echo.
pause
