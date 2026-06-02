# rpa-prototype

Lightweight RPA prototype that uses Playwright to log in to a site, scrape quotes, and store results as CSV and in a SQLite database.

**Project layout**
- `main.py` — orchestrates login, scraping, and persistence.
- `automation/` — Playwright helpers and scrapers (`browser.py`, `login.py`, `scraper.py`).
- `database/db_handler.py` — SQLite helpers to initialize DB and insert quotes.
- `tasks/celery_worker.py` — example Celery task for async scraping.
- `requirements.txt` — Python dependencies.
- `Extra/Dockerfile`, `Extra/docker-compose.yml` — containerization examples.
- `output/` — saved CSV/DB output (quotes.csv, quotes.db).

Features
- Browser automation with Playwright (synchronous API).
- Scrapes https://quotes.toscrape.com and saves data to CSV and SQLite.
- Optional Celery task wrapper for background execution.
- Dockerfile and docker-compose example for containerized runs.

Requirements
- Python 3.9+ (Dockerfile uses 3.9-slim)
- Chrome/Chromium (Playwright will install browsers when run)
- Redis (if using Celery tasks)

Setup (local)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

3. Environment variables
- The project reads credentials from `credentials` module. You can either:
  - Edit `credentials/__init__.py` and set `LOGIN_URL`, `USERNAME`, `PASSWORD`; or
  - Replace the `credentials` import with `python-dotenv` usage and a `.env` file.
- For Celery, set `REDIS_URL` (defaults to `redis://localhost:6379/0`).

4. Run the app

```bash
python main.py
```

This will:
- Initialize the SQLite DB (path currently set in `database/db_handler.py`).
- Launch a non-headless browser, perform login, scrape quotes, save CSV in `output/`, and insert rows into the DB.

Docker (optional)
- A Dockerfile and `docker-compose.yml` example are provided under `Extra/`.
- To build and run (from project root):

```bash
docker build -f Extra/Dockerfile -t rpa-prototype:latest .
docker run --rm -it -v %cd%/output:/app/output rpa-prototype:latest
```

Or with docker-compose (from project root):

```bash
docker-compose -f Extra/docker-compose.yml up --build
```

Celery notes
- `tasks/celery_worker.py` contains a sample Celery app using `REDIS_URL`.
- To run worker:

```bash
celery -A tasks.celery_worker.celery_app worker --loglevel=info
```

Important implementation notes
- `automation/scraper.py` and `database/db_handler.py` currently use an absolute Windows path for `output` and DB (C:\Users\ASUS\Prototype\rpa-prototype\output). Consider changing to a project-relative path or reading it from env to make the project portable.
- `main.py` uses the synchronous Playwright API and keeps the browser open until user input. For headless automated runs, modify `automation/browser.py` to launch headless and remove the `input()` pause.

Where results are stored
- CSV: `output/quotes.csv`
- SQLite DB: `output/quotes.db`

Next steps / Suggestions
- Convert hardcoded Windows paths to relative paths (Path(__file__).resolve().parents).
- Move secrets to `.env` and use `python-dotenv` or environment variables.
- Add unit tests for `database/db_handler.py` and `automation/scraper.py`.

If you want, I can:
- Open a PR that converts hardcoded paths to relative/project paths.
- Add a `.env.example` and update `credentials` to use `python-dotenv`.

