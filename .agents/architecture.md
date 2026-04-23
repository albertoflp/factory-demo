# Architecture

Empty on purpose — this file grows as features ship. After each meaningful change
(new Django app, new frontend module, new data relationship), the Feature Builder
should update this file in the same commit.

## Data model

*Nothing yet. Add an ERD / entity list here as models are introduced.*

## Apps

| App                | Purpose                                                       |
| ------------------ | ------------------------------------------------------------- |
| `apps.accounts`    | Authentication endpoints. Uses Django's built-in `User` model and DRF `SessionAuthentication`. |

## API surface

| Method | Path                | View                              | Purpose                                  |
| ------ | ------------------- | --------------------------------- | ---------------------------------------- |
| GET    | `/api/health/`      | `config.views.health`             | Liveness + DB ping. 200 on healthy, 503 when the DB is unreachable. |
| POST   | `/api/auth/login/`  | `apps.accounts.views.login_view`  | Authenticate with `{username, password}`. 200 + `{id, username, is_staff}` + session cookie on success; 400 on missing fields; 401 on bad credentials. |
| GET    | `/api/auth/me/`     | `apps.accounts.views.me_view`     | Return the current user as `{id, username, is_staff}`. 401 if unauthenticated. |

## Frontend routes

*Nothing yet. Add route table here as pages are introduced.*

## Key decisions

- **Backend layout**: Django project package lives at `backend/config/` with per-domain apps under `backend/apps/`. Project-level URLs are routed from `config/urls.py`; project-level one-off views (like `/api/health/`) live in `config/views.py`. Domain apps own their own `urls.py` and are mounted under `/api/<name>/`.
- **Database config**: `DATABASE_URL` parsed via `dj-database-url` in `config/settings.py`. Defaults to the docker-compose Postgres (`postgres://factory_demo:factory_demo@localhost:5432/factory_demo`). `SECRET_KEY` comes from env with a dev-only default.
- **Auth**: DRF defaults to `SessionAuthentication` + `BasicAuthentication`. The SPA (Vite dev server at `http://localhost:5173`) is whitelisted via `django-cors-headers` (`CORS_ALLOWED_ORIGINS`, `CORS_ALLOW_CREDENTIALS=True`) and `CSRF_TRUSTED_ORIGINS`. No token/JWT auth yet.
