System Architecture

Overview
- Client: React (TypeScript), SPA with React Router and React Query.
- API: Python FastAPI service (REST + WebSocket later), containerized.
- Database: PostgreSQL for relational data, strong consistency.
- Cache/Queue: Redis for caching, rate limiting, and Celery task broker.
- Object Storage: S3‑compatible (e.g., AWS S3/MinIO) for images.
- Background Workers: Celery workers for image processing, notifications, fanout.
- Search: Postgres full‑text search initially; optional OpenSearch later.
- CDN: CDN in front of image bucket for low‑latency delivery.
- Observability: OpenTelemetry, Prometheus metrics, structured logs.

Runtime Components
- Web: NGINX or CDN terminates TLS, serves static FE build, proxies API.
- App API: FastAPI app instances behind a load balancer.
- Workers: Celery workers and beat scheduler for recurring jobs.
- Data Layer: PostgreSQL primary (HA possible) and Redis cluster if needed.
- Storage: S3/MinIO bucket with lifecycle policies; image transforms stored as variants.

High‑Level Data Flow
1. User requests FE → CDN/NGINX serves SPA.
2. SPA calls API → FastAPI authenticates, authorizes, queries Postgres, leverages Redis cache, returns JSON.
3. Uploads: client uploads images to pre‑signed S3 URLs; API stores metadata; Celery generates variants (thumb/medium).
4. Feed/Search: API queries Postgres with filters and FTS; caches popular queries.
5. Notifications: writes event → Celery processes and stores notifications; in‑app fetch; later WebSocket push.

Deployment Topology
- Dev: docker‑compose (API, Postgres, Redis, MinIO, worker, NGINX).
- Staging/Prod: containers on cloud (ECS/Kubernetes) + managed Postgres + managed Redis + S3 + CDN.

Monorepo Structure (suggested)
/
  frontend/            React app (Vite)
  backend/             FastAPI app + Celery
  infra/               Docker, compose, IaC (optional)
  docs/                Additional diagrams/specs (optional)

Key Trade‑Offs
- Python FastAPI vs Node/NestJS: Choosing FastAPI for Python ecosystem strength (data, async, type hints) and straightforward async support; either is viable. If team prefers TS end‑to‑end, NestJS + Prisma is a solid alternative.
- Search: Start with Postgres FTS for simplicity; upgrade to OpenSearch if query complexity/scale demands.
- Realtime: Start with in‑app polling; upgrade to WebSockets for messaging/notifications when needed.

