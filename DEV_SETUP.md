Developer Setup

Local (docker‑compose)
- Requirements: Docker Desktop, make (optional), Node 20+, Python 3.12 (optional if not using Docker for dev commands).
- Services: Postgres, Redis, MinIO, FastAPI app, Celery worker, frontend dev server, NGINX.

Suggested Commands (to be implemented in repo)
- make up — start all services
- make logs — tail logs
- make down — stop and remove
- make migrate — run Alembic migrations
- make seed — load sample data

Environment
- Create `.env` files for backend and frontend with defaults:
  - BACKEND: DATABASE_URL, REDIS_URL, S3_ENDPOINT, S3_BUCKET, S3_ACCESS_KEY, S3_SECRET_KEY, JWT_SECRET, APP_ENV, CORS_ORIGINS
  - FRONTEND: VITE_API_BASE_URL, VITE_APP_ENV

Local Image Uploads
- Use MinIO with a local bucket; presigned uploads from backend; store keys only.

Running Tests
- Backend: `pytest -q` (with test containers) and `ruff check . && black --check .`
- Frontend: `pnpm test` and `pnpm lint`

Git Hooks (optional)
- pre‑commit with ruff/black/eslint/prettier and basic security checks.

