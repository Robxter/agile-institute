# Contracts (owner: lead-architect)

Written from the code on 2026-11-25. If code and this file disagree, the code wins and this file gets fixed.

## 1. Public origin (Render `agile-landing`, Node BFF — `front-end/server/index.mjs`)

| Method | Path | Handled by | Contract |
| --- | --- | --- | --- |
| POST | `/api/pilot-requests` | BFF | Body JSON ≤ 16 KB: `{ name, email, organization, size?, message?, consent: true, website? }`. `size` ∈ `<50`, `50-250`, `250-1000`, `>1000`; `message` ≤ 1000 chars; `website` is a honeypot (filled → fake `201`). `201 { id }` · `422 { error, fields }` · `400` bad JSON · `413` too large. On `201` the record is appended to `data/pilot-requests.jsonl`, then emails are sent (§4). |
| GET | `/api/health` | BFF | `200 { status: "ok", cdm: "up" \| "down" \| "http <code>" }` |
| GET | `/app` | proxy → CDM `/` | Centro de mando UI (same origin, so its `SameSite=strict` cookie works) |
| * | `/static/*`, other `/api/*` | proxy → CDM | Forwarded with method, headers, body and `set-cookie`; `502 { error }` if CDM is down |
| GET | anything else | BFF | `dist/` SPA, falling back to `index.html` |

## 2. Centro de mando API (Render private service — `centro-de-mando/app/main.py`)

Session: cookie set by login (`httponly`, `samesite=strict`), in-memory sessions (lost on restart).
Common filters (query): `tipo` (`DEMO`/`REAL`), `periodo` (`YYYY-MM`), `organizacion`, `equipo`, `persona`.
Scope rules: `ROLE_DASHBOARDS` and `MIN_GROUP` in `app/dashboard.py` (403 when out of scope, 400 on bad filters).

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/auth/demo-accounts` | Demo accounts; only when `CDM_DEMO_LOGIN=1` |
| POST | `/api/auth/login` | `{ email }`; demo login only when `CDM_DEMO_LOGIN=1` |
| POST | `/api/auth/logout` | Clears the session |
| GET | `/api/auth/me` | Current user, role, permissions |
| GET | `/api/overview` | Cards per authorized dashboard |
| GET | `/api/dashboard/{key}` | `key` ∈ `persona`, `equipo`, `liderazgo`, `organizacion`, `ia`, `persona_ia`, `liderazgo_ia` |
| PUT | `/api/dashboard/{key}/plan` | Editable development plan |
| GET | `/api/dashboard/{key}/export.xlsx` | Excel; `include_data=true` + reason only for admin |
| POST | `/api/import` | `.xlsx` upload; admin only |
| GET/PUT/DELETE | `/api/layout/{key}` | Per-user dashboard layout |
| GET | `/api/audit` | Last 50 audit entries; admin only |
| GET | `/` | UI (`static/index.html`) |

## 3. Landing content model (`front-end/src/content/landing.ts`)

- `dimensions[].key` and `views.items[].key` are `DimensionKey` and must match the dashboard keys in §2.
- `views.items[].key = null` links to the centro de mando home (`/app`).
- All copy lives in `landing.ts`; brand is "Agile Institute™".

## 4. Email (Resend — `front-end/server/mail.mjs`)

`POST https://api.resend.com/emails`, `Authorization: Bearer $RESEND_API_KEY`, body
`{ from, to[], subject, html, text, reply_to? }`, header `idempotency-key`. Per pilot request: team notice
(`pilot-team-<id>`, to `MAIL_TEAM_TO`, reply-to requester) and requester acknowledgement (`pilot-ack-<id>`).

## 5. Environment variables

| Variable | Service | Default | Purpose |
| --- | --- | --- | --- |
| `PORT` / `BFF_PORT` | landing | `5174` | BFF port |
| `CDM_API_URL` | landing | `http://127.0.0.1:8765` | CDM base (accepts `host:port`) |
| `VITE_APP_URL` | landing (build) | `/app` | CDM link target |
| `RESEND_API_KEY`, `MAIL_FROM`, `MAIL_TEAM_TO` | landing | — | Email; unset → no email sent |
| `CDM_DB_PATH` | CDM | `data/centro_mando.db` | SQLite file |
| `CDM_CATALOG_PATH` | CDM | design workbook in `Mejora/` | Item catalog |
| `CDM_MIN_GROUP` | CDM | `5` (never below 5) | Anonymity threshold |
| `CDM_DEMO_LOGIN` | CDM | `1` | Demo login; set `0` before real data |
