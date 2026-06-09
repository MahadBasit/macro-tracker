# Macro Tracker

Track daily protein, carbs, fat, and calorie intake against personal goals.

**Live:** https://macro-tracker-one-flax.vercel.app

---

## Features

- Email/password authentication
- Log meals manually — name, protein, carbs, fat, calories
- Dashboard showing today's totals vs daily goals with progress bars
- Set and update daily macro goals

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Nuxt 3, Vue 3, Tailwind CSS |
| Backend | Python Flask |
| Database + Auth | Supabase (PostgreSQL) |
| Frontend deploy | Vercel |
| Backend deploy | Render |

---

## Local Setup

### Prerequisites

- Node.js 18+
- Python 3.11+

### Frontend

```bash
cd frontend
cp .env.example .env   # fill in values
npm install
npm run dev            # http://localhost:3000
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
flask run              # http://localhost:5000
```

---

## Environment Variables

### `frontend/.env`

```
NUXT_PUBLIC_SUPABASE_URL=
NUXT_PUBLIC_SUPABASE_ANON_KEY=
NUXT_PUBLIC_API_BASE=
```

### `backend/.env`

```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
FRONTEND_ORIGIN=
FLASK_ENV=
```

---

## Deployment

- **Frontend** — deploy `frontend/` to Vercel; set the three `NUXT_PUBLIC_*` env vars
- **Backend** — deploy `backend/` to Render as a Python web service; set the four backend env vars, set `FRONTEND_ORIGIN` to your Vercel URL
- **Database** — Supabase project with `meals` and `daily_goals` tables (see SQL below)

### Database Schema

```sql
create table meals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  name text not null,
  protein numeric not null,
  carbs numeric not null,
  fat numeric not null,
  calories numeric not null,
  logged_at timestamptz default now()
);

create table daily_goals (
  user_id uuid references auth.users primary key,
  protein numeric not null,
  carbs numeric not null,
  fat numeric not null,
  calories numeric not null
);

create index meals_user_logged_idx on meals (user_id, logged_at);

alter table meals enable row level security;
alter table daily_goals enable row level security;

create policy "own meals" on meals
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own goals" on daily_goals
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
```
