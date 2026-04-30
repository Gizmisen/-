@echo off
setlocal
cd /d %~dp0

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend\requirements.txt

start "PMZ API" cmd /k "set PYTHONPATH=backend && python backend\run_pmz.py"
timeout /t 2 >nul
start "" http://localhost:8000/
