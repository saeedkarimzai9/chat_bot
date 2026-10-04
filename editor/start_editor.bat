@echo off
title System Edit
cd /d "%~dp0"
where npm >nul 2>nul
if errorlevel 1 (
  echo Node.js/npm is required.
  echo Install Node.js, then run this file again.
  pause
  exit /b 1
)
if not exist node_modules (
  echo Installing System Edit dependencies...
  call npm install
  if errorlevel 1 (
    echo npm install failed.
    pause
    exit /b 1
  )
)
call npm start
