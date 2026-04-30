@echo off
setlocal
cd /d %~dp0

if not exist dist\pmz-ai-control.exe (
  echo EXE not found. Building first...
  call build_exe.bat
)

start "PMZ AI Control" dist\pmz-ai-control.exe

timeout /t 2 >nul
start "" http://localhost:8000/
exit /b 0
