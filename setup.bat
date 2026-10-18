@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (where python >nul 2>nul & if errorlevel 1 (echo Python 3.11+ not found. Install from https://www.python.org/downloads/ and enable Add Python to PATH.& pause & exit /b 1) else (set PY=python)) else (set PY=py -3)
%PY% --version
if errorlevel 1 (echo Python check failed.& pause & exit /b 1)
if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
if errorlevel 1 (echo Could not create virtual environment.& pause & exit /b 1)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (echo pip upgrade failed.& pause & exit /b 1)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (echo Dependency installation failed. Check internet access.& pause & exit /b 1)
".venv\Scripts\python.exe" -m flask --app app init-db
if errorlevel 1 (echo Database initialization failed.& pause & exit /b 1)
".venv\Scripts\python.exe" -m flask --app app seed
if errorlevel 1 (echo Sample seeding failed.& pause & exit /b 1)
echo Setup complete. Run run.bat to start Kahani Adda.
pause
