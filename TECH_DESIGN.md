Technical Design

Tech Stack
- Frontend: React 18 + TypeScript, Vite, React Router, React Query, Tailwind CSS + Headless UI, React Hook Form + Zod.
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.x (async), Alembic for migrations, Pydantic v2.
- Background: Celery + Redis broker; scheduled tasks via Celery Beat.
- Database: PostgreSQL 15+; pgvector optional later for recommendations.
- Cache/Rate Limiting: Redis.
- Storage: S3 (or MinIO in dev) with presigned PUT for uploads.
- Auth: JWT access + refresh (rotating), HTTP‑only cookies, OAuth (Google/Apple later via Authlib).
- Observability: OpenTelemetry, Prometheus, Sentry (or equivalent) for error tracking.
- CI/CD: GitHub Actions; Docker images; deploy to ECS/Kubernetes.

API Design Principles
- RESTful resources, predictable pagination (cursor preferred), filtering via query params, sparse fieldsets where helpful.
- Idempotent writes for safe retries (e.g., conditional updates with If‑Match/ETag later).
- Validation at edges with Pydantic schemas; consistent error envelopes.
- Versioning: /api/v1 with evolution via additive changes; breaking changes via new version.

Authentication & Authorization
- AuthN: email/password with password hashing (argon2); email verification; password reset via token.
- Sessions: JWT access (short‑lived) + refresh (longer‑lived) in secure, HTTP‑only cookies; CSRF tokens for state‑changing endpoints if cookies used cross‑site.
- AuthZ: role‑based (user, moderator, admin) + ownership checks per resource. Fine‑grained checks via dependency injections in FastAPI.

Key Services & Modules (Backend)
- app/main.py: FastAPI entrypoint, routers mount, middleware (CORS, sessions, logging).
- app/config.py: pydantic‑settings for env configuration.
- app/db.py: async engine/session management; Alembic migration runner.
- app/models/: SQLAlchemy models and enums.
- app/schemas/: Pydantic request/response models.
- app/routers/: route modules (auth, users, profiles, items, feed, search, social, comments, notifications).
- app/services/: business logic (image, feed ranking stub, notifications, follows/likes logic).
- app/tasks/: Celery tasks (image processing, notification fanout, cleanup).
- app/security/: auth utils, password hashing, JWT issuing/validation.
- app/storage/: S3 client wrapper and presigned URL creation.
- app/observability/: metrics, tracing, and logging config.

Image Handling
- Client uploads via presigned PUT to S3; backend stores object keys and metadata.
- Celery generates variants (thumbnail, medium) and writes back with deterministic keys.
- Serve via CDN; include width/height/aspect in API responses for layout stability.

Feed & Search
- MVP feed: reverse‑chronological from followed users + popularity fallback.
- Search: Postgres FTS on title/description + faceted filters on brand/category/size/price/location.
- Indexes: composite indexes on (user_id, created_at), (category, price), (brand), GIN index for FTS.

Notifications
- Event table (append‑only) + notifications table per user.
- In‑app polling first; WebSockets channel once messaging lands.

Performance & Caching
- Use ETags/Last‑Modified on list endpoints; client conditional requests.
- Cache hot queries in Redis with short TTL; invalidate on writes affecting result sets.
- N+1 avoidance with SQLAlchemy eager loading where sensible.

Error Handling
- Global exception handlers returning structured errors {error: {code, message, details}}.
- Correlate logs with request IDs; include user_id if present.

Alternative Backend (if TypeScript end‑to‑end preferred)
- NestJS + Prisma + PostgreSQL, BullMQ for background jobs, Zod + class‑validator, Passport for auth.
- Trade‑offs: unified language in FE/BE; strong DX; similar architecture otherwise.

