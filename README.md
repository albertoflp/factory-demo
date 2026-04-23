# factory-demo

A minimal admin dashboard, built by AI agents as an end-to-end test of an
autonomous development loop.

## Stack

- **Frontend:** React + Vite + TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod
- **Backend:** Django + Django REST Framework
- **Data:** PostgreSQL (Redis will be added later when something needs it)

## Run locally

```bash
docker compose up -d          # Postgres
cd backend && # (see backend/README.md once scaffolded)
cd frontend && # (see frontend/README.md once scaffolded)
```

## How work happens

This repo is driven by two autonomous agents running on a VM:

- **Feature Builder** picks the next `status:backlog` issue every 10 min and opens a PR.
- **PR Reviewer** reviews / fixes CI / merges every 5 min.

Human input: file an issue (or comment on one), or push to a branch with the `ona-user` label.
