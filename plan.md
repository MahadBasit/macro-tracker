# Macro Tracker — V1 Implementation Blueprint (PROMPT 1 / Planning)

## Context

Greenfield build. Repo currently holds only `CLAUDE.md`, `LICENSE`, `README.md` — no `frontend/` or `backend/` directories exist yet. This plan is the full scaffold blueprint for a V1 macro-tracking web app: authenticated users log meals manually (name + protein/carbs/fat/calories) and view today's totals against personal daily goals.

Hard scope from `CLAUDE.md` (do not exceed):
- **In:** email/password auth (Supabase), log a meal, dashboard (today's totals vs goals), set daily goals (one-time).
- **Out:** food DB search, meal history/past days, charts, mobile polish, social.

---

## 1. Folder & File Structure

### `/frontend` — Nuxt 3 + Vue 3 + Tailwind

```
frontend/
├── nuxt.config.ts          # Modules (@nuxtjs/supabase, @nuxtjs/tailwindcss), supabase url/key from NUXT_PUBLIC_* env, runtimeConfig.public.apiBase, auth redirect options
├── package.json            # deps: nuxt, vue, @nuxtjs/supabase, @nuxtjs/tailwindcss
├── tsconfig.json           # extends .nuxt/tsconfig (auto-generated)
├── .env                    # NUXT_PUBLIC_SUPABASE_URL, NUXT_PUBLIC_SUPABASE_ANON_KEY, NUXT_PUBLIC_API_BASE (gitignored)
├── .env.example            # same keys, empty values (committed)
├── app.vue                 # Root: <NuxtLayout><NuxtPage/></NuxtLayout>
├── assets/css/main.css     # Tailwind @tailwind directives
├── composables/
│   └── useApi.ts           # $fetch wrapper: prefixes apiBase, injects "Authorization: Bearer <access_token>" from current session; central place for all Flask calls
├── layouts/
│   └── default.vue         # Top nav: app name, current user email, logout button (supabase.auth.signOut)
├── middleware/
│   └── auth.global.ts      # Guard: redirect unauthenticated users to /login; excludes /login, /signup
├── pages/
│   ├── login.vue           # Email+password sign-in form → supabase.auth.signInWithPassword; link to /signup
│   ├── signup.vue          # Email+password registration → supabase.auth.signUp; on success route to /login or /goals
│   ├── index.vue           # Dashboard. Fetches GET /api/goals + GET /api/meals/today. If no goals → redirect /goals. Renders MacroSummary + MealForm + MealList
│   └── goals.vue           # Set/edit daily macro goals form → POST /api/goals; prefills from GET /api/goals
└── components/
    ├── MealForm.vue        # Inputs: name, protein, carbs, fat, calories. Submits POST /api/meals, emits "logged" to trigger dashboard refresh
    ├── MacroSummary.vue    # Props: totals + goals. Renders consumed/goal per macro (protein/carbs/fat/calories) with a simple progress bar
    └── MealList.vue        # Props: meals[]. Lists today's logged meals (name + macro breakdown)
```

### `/backend` — Flask REST API

```
backend/
├── app.py                  # App entry: create Flask app, init CORS, register meals + goals blueprints
├── .flaskenv               # FLASK_APP=app.py, FLASK_ENV=development
├── requirements.txt        # flask, flask-cors, supabase, pyjwt, python-dotenv
├── .env                    # SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_JWT_SECRET, FRONTEND_ORIGIN, FLASK_ENV (gitignored)
├── .env.example            # same keys, empty values (committed)
├── config.py               # Loads + validates env vars at import; raises if a required secret is missing
├── supabase_client.py      # Singleton supabase-py client built with service key
├── auth.py                 # @require_auth decorator: extract Bearer token, verify JWT (PyJWT HS256), set g.user_id; returns 401 on failure
├── validation.py           # validate_meal(payload) + validate_goals(payload): required fields, numeric, >= 0
└── routes/
    ├── __init__.py
    ├── meals.py            # Blueprint: POST /api/meals, GET /api/meals/today
    └── goals.py            # Blueprint: POST /api/goals (upsert), GET /api/goals
```

---

## 2. Supabase Setup

### Tables (run in Supabase SQL editor)

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
```

### RLS Policies

```sql
alter table meals enable row level security;
alter table daily_goals enable row level security;

create policy "own meals" on meals
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own goals" on daily_goals
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
```

### Key Usage

| Key | Where | Used for |
|-----|-------|----------|
| **anon key** | frontend only | supabase-js auth: signUp / signInWithPassword / signOut / session refresh |
| **service key** | backend only | supabase-py: all meal + goal reads/writes, scoped by verified user_id in code |
| **JWT secret** | backend only | verify access token signature to extract user_id |

---

## 3. Auth Flow

1. User submits email/password on `/login`. Frontend calls `useSupabaseClient().auth.signInWithPassword({ email, password })`.
2. `@nuxtjs/supabase` persists the session and auto-refreshes tokens. `useSupabaseUser()` becomes reactive.
3. For any Flask call, `useApi.ts` reads the live session and sets `Authorization: Bearer ${session.access_token}`.
4. Flask `@require_auth` in `auth.py` verifies: `jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")`. On success sets `g.user_id = payload["sub"]`; on failure returns `401`.
5. Route handlers read `g.user_id` and scope every DB operation to it. Frontend never sends `user_id` — derived only from the verified token.

---

## 4. API Design

Consistent envelope: success → `{ "data": <payload> }`; error → `{ "error": "<message>" }`. All routes require `Authorization: Bearer <token>`; missing/invalid → `401`.

### POST `/api/meals`
- **Body:** `{ name: string, protein: number, carbs: number, fat: number, calories: number }`
- **Validation:** name non-empty; four macros present, numeric, >= 0
- **201:** `{ "data": { id, name, protein, carbs, fat, calories, logged_at } }`
- **Errors:** 400 (validation), 401, 500

### GET `/api/meals/today`
- **Action:** select meals where user_id = g.user_id and logged_at within today's UTC day
- **200:** `{ "data": [ { id, name, protein, carbs, fat, calories, logged_at }, ... ] }`
- **Errors:** 401, 500

### POST `/api/goals`
- **Body:** `{ protein: number, carbs: number, fat: number, calories: number }`
- **Validation:** four macros present, numeric, >= 0
- **Action:** upsert into daily_goals keyed on user_id
- **200:** `{ "data": { user_id, protein, carbs, fat, calories } }`
- **Errors:** 400, 401, 500

### GET `/api/goals`
- **Action:** select daily_goals where user_id = g.user_id
- **200:** `{ "data": { protein, carbs, fat, calories } }` or `{ "data": null }` if not set
- **Errors:** 401, 500

---

## 5. Frontend Pages & Components

| File | Fetches | Triggers | Renders |
|------|---------|----------|---------|
| `pages/login.vue` | — | `auth.signInWithPassword` | email/password form, error msg, link to signup |
| `pages/signup.vue` | — | `auth.signUp` | email/password form, success/error msg |
| `pages/index.vue` | `GET /api/goals`, `GET /api/meals/today` | refresh on meal logged; redirect to `/goals` if goals null | `MacroSummary`, `MealForm`, `MealList` |
| `pages/goals.vue` | `GET /api/goals` (prefill) | `POST /api/goals` → route to `/` | goals form (4 numeric inputs) |
| `components/MealForm.vue` | — | `POST /api/meals`, emit `logged` | name + 4 numeric inputs, submit |
| `components/MacroSummary.vue` | — (props) | — | per-macro consumed/goal + progress bar |
| `components/MealList.vue` | — (props) | — | list of today's meals |
| `layouts/default.vue` | `useSupabaseUser()` | `auth.signOut` → `/login` | nav: app name, user email, logout |

---

## 6. State Management

No Pinia. Page-scoped data only.

- **Session:** `useSupabaseUser()` — reactive, app-global, provided by `@nuxtjs/supabase`
- **Today's meals + goals:** owned by `pages/index.vue` via `useAsyncData('dashboard', ...)`. `MealForm` emits `logged` → page calls `refresh()` → totals recompute. Data flows down via props, events flow up via emits.
- **Goals editing:** `pages/goals.vue` fetches its own copy for prefill; after POST navigates to `/`.

---

## 7. Assumptions

1. Greenfield scaffold — repo has only `CLAUDE.md`, `LICENSE`, `README.md`.
2. Auth integration: `@nuxtjs/supabase` module (handles cookie session, SSR, token refresh, route redirect).
3. JWT verification: PyJWT local HS256 with `SUPABASE_JWT_SECRET` (no per-request network round trip).
4. DB access (backend): `supabase-py` client with service key (parameterized PostgREST calls).
5. Totals computed client-side in `MacroSummary`.
6. "Today" boundary: UTC calendar day.
7. Email confirmation: disabled in Supabase Auth settings for dev.
8. Versions: Nuxt 3.x / Node 18+, Python 3.11+ / Flask 3.x, supabase-py v2.
9. Goals = single row per user, managed via upsert.

---

## 8. Potential Blockers & Resolutions

| Blocker | Resolution |
|---------|-----------|
| **CORS** | `flask-cors`: `CORS(app, origins=[FRONTEND_ORIGIN], allow_headers=["Authorization","Content-Type"])`. `FRONTEND_ORIGIN` from env: `http://localhost:3000` dev, Vercel URL prod. |
| **JWT verification** | PyJWT `decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")`. Catch `ExpiredSignatureError` / `InvalidTokenError` → 401. |
| **Supabase RLS** | RLS + `auth.uid() = user_id` policies on both tables. Service key backend bypasses RLS and enforces `user_id` in code. |
| **Env var wiring** | frontend/.env: `NUXT_PUBLIC_SUPABASE_URL`, `NUXT_PUBLIC_SUPABASE_ANON_KEY`, `NUXT_PUBLIC_API_BASE`. backend/.env: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_JWT_SECRET`, `FRONTEND_ORIGIN`, `FLASK_ENV`. `.env.example` committed for both. |
