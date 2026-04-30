@echo off
setlocal
cd /d %~dp0

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
pip install pyinstaller

pyinstaller --onefile --name pmz-ai-control backend\run_pmz.py

echo.
echo EXE created: dist\pmz-ai-control.exe
echo Run it and open http://localhost:8000
pause
