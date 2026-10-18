# Kahani Adda
A mobile-first Flask/Jinja story site for Hindi, Hinglish and English. Local database: SQLite. Production: set `DATABASE_URL` to persistent PostgreSQL.

## Requirements
Windows 10/11, Python 3.11+, internet for dependency install, Git/GitHub for deployment.

## Run locally in PowerShell
Extract to `C:\AbhijeetProjects\Kahani_Adda`, open PowerShell in that folder, then run:
```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe -m flask --app app seed
.\.venv\Scripts\python.exe -m flask --app app run
```
Open http://127.0.0.1:5000. Or double-click `setup.bat`, then `run.bat`.

## First admin and first story
Run `\.venv\Scripts\python.exe -m flask --app app create-admin` in PowerShell and enter a username plus a unique password of at least 12 characters when prompted. Sign in at `/admin/login`. Dashboard → Create story; choose Published or Draft. Reader submissions remain pending until reviewed.

## Tests
`\.venv\Scripts\python.exe -m unittest discover -s tests -v`

## GitHub
Create an empty repository on GitHub, then run:
```powershell
git init
git add .
git status
git commit -m "Initial Kahani Adda release"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/kahani-adda.git
git push -u origin main
```
Review `git status`; `.env` and database files are ignored. Never commit passwords, `.env`, backups or private submissions.

## Deployment
Choose a currently available GitHub-connected Python host with persistent PostgreSQL. Check current price, free limits, card requirements and storage behavior before creating resources. Build: `pip install -r requirements.txt`. Start: `gunicorn app:app --workers 2 --timeout 120`. Set `DATABASE_URL` to the provider PostgreSQL URL, `SECRET_KEY` to a generated long random secret (`py -c "import secrets; print(secrets.token_urlsafe(48))"`), `SITE_URL` to the exact public HTTPS URL, `COOKIE_SECURE=1`, and `FLASK_DEBUG=0`. In a secure host shell run `flask --app app init-db`, `flask --app app seed`, and `flask --app app create-admin`. Verify story and submission persistence after restarting the service. Do not use SQLite on an ephemeral filesystem. This package does not create a hosting account or claim a live URL has been deployed.

## Backups
For local SQLite, stop the app and copy `kahani_adda.db` somewhere private. Restore with the app stopped. Production PostgreSQL backups should use provider tools or `pg_dump`; test restores. `init-db` doesn't delete data and `seed` skips existing sample slugs.

## Security and external setup
CSRF protection, hashed passwords, server-side validation and security headers are included. The login cooldown is basic; use host/WAF rate limits too. Review policies and obtain a professional security audit before handling significant traffic. Privacy/terms are starter text requiring review. AdSense is not active; see `docs/ADSENSE.md`. Automatic translation is not active; see `docs/TRANSLATION.md`.
