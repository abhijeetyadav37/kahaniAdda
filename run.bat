@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo Virtual environment not found. Run setup.bat first.& pause & exit /b 1)
".venv\Scripts\python.exe" -m flask --app app init-db
if errorlevel 1 (echo Database initialization failed.& pause & exit /b 1)
".venv\Scripts\python.exe" -m flask --app app run --host 127.0.0.1 --port 5000
pause
