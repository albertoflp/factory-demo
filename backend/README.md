# Backend

Django 5 + Django REST Framework, Python 3.13, PostgreSQL 16.

## Install

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Environment

Optional env vars (sensible dev defaults are provided):

- `DATABASE_URL` — defaults to `postgres://factory_demo:factory_demo@localhost:5432/factory_demo`
- `SECRET_KEY` — defaults to a dev-only placeholder
- `DJANGO_DEBUG` — defaults to `True`
- `DJANGO_ALLOWED_HOSTS` — comma-separated, defaults to `localhost,127.0.0.1`

## Run

Start Postgres via docker-compose (from the repo root) and apply migrations:

```bash
docker compose up -d db
cd backend
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Health check: `curl http://localhost:8000/api/health/` →
`{"status": "ok", "db": "ok"}`.

## Create an admin user

After running migrations, create a superuser to log in to the Django admin and
to exercise the `/api/auth/login/` endpoint:

```bash
cd backend
source .venv/bin/activate
python manage.py createsuperuser
```

You can then sign in at `http://localhost:8000/admin/` or POST to
`/api/auth/login/` with `{"username": "...", "password": "..."}`.

## Test

```bash
cd backend
source .venv/bin/activate
pytest
ruff check .
```
