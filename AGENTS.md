# AGENTS.md

This repository is agent-built. Read this file first every run.

## Stack

- **Frontend:** React 18+ + Vite + TypeScript (strict), Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod
- **Backend:** Django 5+ + Django REST Framework, Python 3.13
- **Data:** PostgreSQL 16 (via docker-compose). Redis is **not** yet part of the stack — add it only when an issue explicitly requires it.

## Project structure

```
backend/           → Django project (manage.py, config/, apps/)
frontend/          → Vite React app (src/, public/)
.agents/           → Agent knowledge base
  conventions.md   → coding patterns — read before writing any code
  architecture.md  → data model + system design (grows over time)
docker-compose.yml → Postgres for local dev and tests
```

## Rules

- **TypeScript**: strict mode, no `any`, no `@ts-ignore`, no `as` casts unless justified with a one-line comment. Named exports only.
- **Python**: type hints on all new code. Follow DRF conventions. No bare `except:`.
- **No ORMs other than Django ORM** on the backend. No custom CSS on the frontend — Tailwind utility classes + shadcn/ui components only.
- **Conventional commits**: `feat|fix|chore|docs|test|refactor(scope): description`
- **PRs with type `feat` or `fix` must reference an issue**: `Closes #N`. `chore:` / `docs:` / `refactor:` PRs do not require an issue.
- **Exception — `ona-user` PRs**: PRs created via interactive sessions may use the `ona-user` label instead of linking an issue. The PR Reviewer merges these without requiring `Closes #N`.
- **Environment variables**: `VITE_` prefix only for browser-safe values.
- **Database changes**: a Django migration in the same PR that adds/changes models.

## Testing

- **Backend**: `pytest` (with `pytest-django`). Unit tests for business logic, integration tests for DRF views using `APIClient`.
- **Frontend**: `vitest` for unit tests. Component tests with `@testing-library/react`.
- **Run before pushing**:
  - Backend: `cd backend && pytest && ruff check .`
  - Frontend: `cd frontend && pnpm lint && pnpm typecheck && pnpm test`
- Skip tests only for trivial layout-only components.

## Backlog

Issues use labels for status, priority, and type:

- **Status**: `status:backlog`, `status:in-progress`, `status:in-review`, `status:done`
- **Priority**: `priority:1` (foundation), `priority:2` (features), `priority:3` (polish)
- **Type**: `feature`, `enhancement`, `chore`, `bug`
- **Flags**: `needs-human` (excludes from automation queue), `ona-user` (PR doesn't need a linked issue)

Lifecycle: `status:backlog` → `status:in-progress` → `status:in-review` → `status:done`

### Label rules

- Only issues labeled `status:backlog` are picked up by the Feature Builder.
- Never create a `status:backlog` issue for work you intend to do yourself — use `status:in-progress` to lock it out.
- Never pick up an issue in any state other than `status:backlog`, even if it looks stalled.

## Queries used by agents

```bash
# next feature to build
gh issue list --label "status:backlog" --label "priority:1" --state open \
  --json number,title,body,labels --jq '[.[] | select(.labels | map(.name) | (contains(["needs-human"])) | not)] | sort_by(.number) | .[0]'

# open non-draft PRs (concurrency guard — ≤3 open)
gh pr list --state open --json isDraft --jq '[.[] | select(.isDraft == false)] | length'
```
