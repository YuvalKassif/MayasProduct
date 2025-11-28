Frontend (React + Vite + TypeScript)

Prerequisites
- Node.js 20+ (npm or pnpm)

Setup
- cd frontend
- npm install
- npm run dev

Env
- Create `.env` in `frontend/` (optional):
  - VITE_API_BASE_URL=http://localhost:8000

Notes
- The backend must allow CORS from `http://localhost:5173` and set cookies.
- The app uses cookie-based auth; ensure requests include credentials.

