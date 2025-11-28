Testing & Quality Strategy

Goals
- Catch regressions early, keep velocity high, and ensure reliability of core flows.

Tooling
- Backend: pytest, coverage.py, httpx test client, factory_boy, faker.
- Frontend: Vitest/Jest, React Testing Library, Playwright for e2e.
- Lint/Format: ruff + black (Python), eslint + prettier (FE).

Test Pyramid
- Unit: services, validators, utilities (fast, isolated).
- Integration: API routes with in‑memory/ephemeral Postgres (test container), Redis, MinIO.
- E2E: critical user journeys (onboarding, create listing, feed, search, like/favorite).

Data & Fixtures
- Migrations run fresh per test session; factories create users/items.
- Seed scripts for local dev demo data.

Quality Gates (CI)
- Static checks: type checks (mypy/pyright), lint.
- Unit + integration tests; minimum coverage threshold (e.g., 80%).
- E2E smoke on staging before prod deploy.

Performance & Load
- k6/Gatling for API latency under expected concurrency; track p95 and error rates.

Security Testing
- Dependency scanning (Dependabot); SAST (semgrep/bandit); secret scanning.
- DAST on staging (OWASP ZAP baseline) for critical paths.

Observability for Quality
- SLIs: request latency, error rate, saturation; SLOs with alerts.

