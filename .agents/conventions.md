# Conventions

Minimal coding patterns. Grow this file when a new pattern emerges that should be replicated.

## Backend (Django + DRF)

### Project layout

```
backend/
├── manage.py
├── pyproject.toml           # ruff, pytest, deps via pip/uv
├── config/                  # Django project package
│   ├── settings.py          # single settings file is fine for this app
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── apps/
    └── accounts/            # one app per domain (start with accounts for auth)
        ├── models.py
        ├── serializers.py
        ├── views.py
        ├── urls.py
        ├── admin.py
        └── tests/
            ├── test_models.py
            └── test_views.py
```

### DRF patterns

- **ViewSets over APIView** when the resource is CRUD-shaped. `APIView` is fine for one-off endpoints (e.g., `/api/auth/login/`).
- **Serializers validate input; views orchestrate.** No business logic in serializers beyond field-level validation.
- **URL routing**: each app owns `apps/<name>/urls.py`, mounted in `config/urls.py` under `/api/<name>/`.
- **Auth**: Use Django's built-in `User` model to start. Token or session auth — pick one and stick with it (default: session auth for the admin UI, token auth for the SPA).
- **Settings**: `DEBUG=False` in production; `SECRET_KEY` from env. Database URL from `DATABASE_URL` env var (use `dj-database-url`).

### Tests

- `pytest-django`, tests live in `apps/<name>/tests/`.
- API tests use `rest_framework.test.APIClient`.
- Every new DRF endpoint gets at least: one happy-path test, one auth-required test (for protected endpoints), one validation-failure test.

## Frontend (Vite + React + TS)

### Project layout

```
frontend/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/              # one file per route
│   ├── components/
│   │   ├── ui/              # shadcn/ui primitives (do not edit directly)
│   │   └── <feature>/       # feature components
│   ├── lib/
│   │   ├── api.ts           # fetch wrapper + TanStack Query client
│   │   ├── schemas/         # Zod schemas mirroring backend serializers
│   │   └── utils.ts
│   └── hooks/
└── public/
```

### React + TanStack Query patterns

- **Query keys are arrays**: `['user', id]`, `['posts', { page }]`. Never string keys.
- **Mutations invalidate queries explicitly**: `queryClient.invalidateQueries({ queryKey: ['user'] })`.
- **No fetching in components** — every network call lives behind a `useQuery` or `useMutation` hook in `src/hooks/`.
- **Zod schemas are the source of truth** for API payload shapes. Parse responses at the network boundary; never trust unparsed JSON.

### React Hook Form + Zod

- Every form uses RHF + `zodResolver`.
- Schema lives in `src/lib/schemas/<feature>.ts`, shared between form validation and response parsing where possible.

### Styling

- Tailwind utility classes only. No custom CSS.
- shadcn/ui components are imported from `src/components/ui/`. Add new ones via `pnpm dlx shadcn@latest add <name>`.

## Commits and PRs

- Conventional commits. Scope is optional but nice: `feat(auth): add login endpoint`.
- Every `feat`/`fix` PR body includes:
  - `Closes #N`
  - `## What` — one paragraph
  - `## How` — one paragraph
  - `## Testing` — what tests were added / how to verify manually
