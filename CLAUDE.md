# macro-tracker

A full-stack macro tracking web app. Users log meals manually, track daily protein/carbs/fat/calorie intake against personal goals.

## Stack
- **Frontend**: Nuxt 3 + Vue 3 + Tailwind CSS — lives in `/frontend`
- **Backend**: Python Flask REST API — lives in `/backend`
- **Database + Auth**: Supabase (email/password auth, Postgres)

## Project Structure
```
macro-tracker/
├── frontend/        # Nuxt 3 app
├── backend/         # Flask API
├── README.md
└── CLAUDE.md
```

## Running Locally
```bash
# Frontend
cd frontend && npm run dev        # runs on localhost:3000

# Backend
cd backend && flask run            # runs on localhost:5000
```

## V1 Scope — build only this
- Email/password auth via Supabase
- Log a meal: name, protein (g), carbs (g), fat (g), calories
- Dashboard: today's totals vs daily goal
- Set daily macro goals (one-time setup)

## Out of Scope for V1 — do not build
- Food database search
- Meal history / past days view
- Charts or graphs
- Mobile responsiveness beyond basic usability
- Social features

## Database Schema
```sql
-- Supabase handles the users table via auth

meals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  name text not null,
  protein numeric not null,
  carbs numeric not null,
  fat numeric not null,
  calories numeric not null,
  logged_at timestamptz default now()
)

daily_goals (
  user_id uuid references auth.users primary key,
  protein numeric not null,
  carbs numeric not null,
  fat numeric not null,
  calories numeric not null
)
```

## API Routes (Flask)
```
POST   /api/meals           — log a meal
GET    /api/meals/today     — get today's meals for current user
POST   /api/goals           — set daily goals
GET    /api/goals           — get current user's goals
```

## Environment Variables
```
# frontend/.env
NUXT_PUBLIC_SUPABASE_URL=
NUXT_PUBLIC_SUPABASE_ANON_KEY=

# backend/.env
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
FLASK_ENV=development
```

## Deployment
- Frontend → Vercel
- Backend → Render
- Database → Supabase (already hosted)
