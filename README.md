# Coffeans

A bean-first discovery app for coffee shops, roasteries, and beans — with a personal cupping journal
that uses Claude to turn loose tasting notes into structured flavor tags.

## Stack

- **Frontend:** React + TypeScript (Vite), React Query, React Router
- **Backend:** FastAPI (async), SQLAlchemy 2.0, Alembic
- **DB:** Postgres
- **AI:** Anthropic API for flavor-note parsing (`app/services/claude_service.py`)

## Project layout

```
coffeans/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + router wiring
│   │   ├── models/            # SQLAlchemy models (User, Roastery, Shop, Bean, TastingEntry)
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── api/                # Route handlers (auth, roasteries, shops, beans, tasting)
│   │   ├── services/
│   │   │   └── claude_service.py   # Anthropic API call for flavor-note parsing
│   │   ├── core/               # Config + JWT/password helpers
│   │   └── db/                 # Session, base, seed script
│   └── alembic/                 # Migrations
└── frontend/
    └── src/
        ├── api/client.ts        # Typed fetch client
        ├── auth/AuthContext.tsx
        └── pages/                # Beans, Shops, Journal, Login, Signup
```

## Getting started

### 1. Configure environment variables

```bash
cd backend
cp .env.example .env
# then fill in ANTHROPIC_API_KEY and a real SECRET_KEY
```

### 2. Run everything with Docker Compose

```bash
docker compose up --build
```

This starts Postgres on `5432`, the FastAPI backend on `8000`, and the Vite dev server on `5173`.

### 3. Run migrations and seed data

Once the containers are up:

```bash
docker compose exec backend alembic revision --autogenerate -m "initial schema"
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.db.seed
```

### 4. Open the app

Visit `http://localhost:5173`. The API docs are at `http://localhost:8000/docs`.

## Running without Docker

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

You'll need a local Postgres instance and to update `DATABASE_URL` in `.env` accordingly.

## Next steps

- **Google Places ingestion** (`app/services/google_places.py` — not yet built): pull shop location/hours from Places API into the `shops` table.
- **Roaster site scraper** (`app/services/scraper.py` — not yet built): pull bean lineups and raw tasting notes from a few roasters you like.
- **Recommendations**: once there's enough tasting-journal data, use it to suggest new beans based on flavor tag overlap.
- **Auth hardening**: current JWT setup is fine for personal/dev use; add refresh tokens and rate limiting before any real deployment.
