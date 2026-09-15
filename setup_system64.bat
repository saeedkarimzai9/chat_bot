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
echo IMPORTANT: the Ollama model is the main large download.
echo If qwen2.5-coder is already installed, nothing else is needed for the AI model.
echo The wake-word listener also needs a small Vosk English model.
echo.
echo Setup finished.
echo Run system64_launcher.bat to start System 64.
echo.
pause
