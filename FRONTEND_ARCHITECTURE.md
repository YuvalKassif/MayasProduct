Frontend Architecture (React)

Overview
- React + TypeScript SPA with Vite build; React Router for routing; React Query for server caching; Tailwind CSS for design system; Headless UI for accessible primitives.

Project Structure (suggested)
frontend/
  src/
    app/               app shell, providers, routing
    features/
      auth/
      profile/
      items/
      feed/
      search/
      social/
      comments/
      notifications/
    components/        reusable UI
    lib/               utils (api client, analytics, storage)
    styles/            tailwind config and globals
  index.html
  vite.config.ts

State & Data
- Server state: React Query for caching, retries, invalidation; normalized by endpoint.
- Client state: lightweight store (Zustand) for UI state; minimal Redux unless needed.
- Forms: React Hook Form + Zod schemas aligned with backend validation.

Routing
- Public routes: landing, login/register, item browse.
- Private routes: create listing, profile edits, favorites.
- Error boundaries and route‑level code splitting.

API Client
- Fetch wrapper using fetch/axios with interceptors for auth and retry on 401 with refresh.
- Type‑safe response models via shared schema generation (optional later using openapi‑typescript).

UI/UX
- Responsive card grid, skeleton loaders, optimistic updates for likes/favorites.
- Accessible components; focus management; keyboard navigability.
- Image components selecting appropriate variant (thumb/medium) with lazy loading.

Performance
- Code splitting per route; prefetch queries on hover; image lazy loading; useMemo/useCallback sparingly.

Testing
- Unit: component logic with React Testing Library.
- Integration: pages with mocked API.
- E2E: Playwright from login → create listing → like/favorite → search.

