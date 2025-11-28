Backend (FastAPI) — MVP Skeleton

Run locally (no Docker)
- Create a virtualenv and install requirements:
  - python -m venv .venv && .venv/Scripts/activate (Windows)
  - pip install -r requirements.txt
- Start the API:
  - uvicorn app.main:app --reload --port 8000

Health check
- GET http://localhost:8000/health → { "status": "ok", "version": "0.1.0" }

Run tests
- pip install -r requirements-dev.txt
- pytest -q

Docker
- Build: docker build -t shc-backend:dev .
- Run: docker run -p 8000:8000 shc-backend:dev

Database & migrations
- The Docker Compose stack provides Postgres at `db:5432` with `DATABASE_URL` set.
- Alembic runs automatically on container start (`alembic upgrade head`).
- Manual migration commands (from `backend/`):
  - Generate: `alembic revision --autogenerate -m "message"`
  - Apply: `alembic upgrade head`
  - Downgrade: `alembic downgrade -1`

DB health check
- GET http://localhost:8000/health/db → { "database": "ok" }
