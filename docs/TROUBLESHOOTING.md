# Troubleshooting
- `py` not found: install Python 3.11+ and enable Add Python to PATH; reopen PowerShell.
- Dependency install fails: check internet/proxy, then rerun `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- Port 5000 busy: run `.\.venv\Scripts\python.exe -m flask --app app run --port 5001`.
- PostgreSQL connection failure: check URL, credentials, SSL and network access.
- Stories disappear after deploy: verify the app uses persistent PostgreSQL, not an ephemeral SQLite file.
- CSRF error: reload the form and submit again.
- Sample duplicates: seed skips existing slugs.
