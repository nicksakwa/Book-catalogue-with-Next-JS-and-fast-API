Local dev notes

This project expects the backend API to be reachable at the URL set in NEXT_PUBLIC_API_URL.

- For local browser development (running `npm run dev` or `next dev` on host):
  - Use `frontend/.env.local` to set NEXT_PUBLIC_API_URL=http://localhost:8000
  - Then restart the Next.js dev server so it picks up the env file.

- When running frontend inside Docker via `docker-compose`:
  - The frontend container can reach the backend container at http://backend:8000 because Docker provides the `backend` hostname on the same network.
  - In that case the Dockerfile sets `ENV NEXT_PUBLIC_API_URL=http://backend:8000` and no change is needed.

If you see CORS errors in the browser console (OPTIONS CORS Failed):
- Make sure the backend lists http://localhost:3000 in the allowed origins (see backend/app/main.py).
- If frontend is served from file:// or a different port, add that origin to `origins`.

Troubleshooting quick steps (host/Windows PowerShell):
1. Ensure backend is running on host: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` from backend/app folder
2. Start frontend dev server from frontend folder: `npm run dev` (Next.js listens on port 3000)
3. Open browser to http://localhost:3000

