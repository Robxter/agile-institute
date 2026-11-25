# Agile Institute™ — project instructions for Claude Code

Agile Institute™ measures the competencies of people, teams, leaders and organizations for agility and a responsible
use of AI. The product is a **pilot instrument**: results are descriptive, for development only, never for selection,
promotion or dismissal, and psychometric validation is in progress.

- Owner and final approver: the user (GitHub `Robxter`).
- Brand: **Agile Institute™** — trademark (™), never copyright (©).
- Agent roster, routing and approval flow: `docs/AGENTS.md`. Tasks: `TASKS.md`. Handoff: `docs/HANDOFF.md`.
- Pending changes requested by the owner: `CHANGES.md`.

## 1. Rule zero: no invented data, no unvalidated claims

1. Every number shown comes from the centro de mando's scoring of real or DEMO responses (`centro-de-mando/app/`),
   from the design workbook in `centro-de-mando/Mejora/`, or is labelled as illustrative ("datos ilustrativos", DEMO).
2. Never claim validity, reliability, accuracy or impact that has not been measured. Copy keeps "piloto",
   "pendiente de validación" and "no para selección, promoción ni despido" wherever results appear.
3. Group results are never shown below the minimum group size (`CDM_MIN_GROUP`, never below 5). Mixed dashboards show
   each questionnaire with its own n; questionnaires are never summed or subtracted; no global index.
4. If a task cannot be done without inventing data or a claim, stop and add an entry to `docs/decisions/PENDING.md`.

## 2. Other absolute rules

- No secrets in code, logs, commits or reports. Secrets live in `.env` (git-ignored) and Render environment variables.
  Never read or print `.env` contents.
- Spanish (Spain) for all user-facing copy; landing copy lives only in `front-end/src/content/landing.ts`.
- Accessibility: WCAG 2.2 AA, keyboard reachable, `prefers-reduced-motion` respected, works at 360 px.
- Corporate palette and tokens in `front-end/src/styles/tokens.css` (Agile Navy `#0B3A4A` …). No ad-hoc colours.

## 3. Architecture

```
Internet ─► agile-landing (Render web, Node 22)                  front-end/
              React 18 + Vite + TS SPA (dist/)                   src/  (content, components, styles, api)
              BFF server/index.mjs (no deps)                     /api/pilot-requests, /api/health
              server/mail.mjs → Resend REST API                  pilot-request emails
              proxy /app, /static/*, /api/* ──private network──► centro-de-mando (Render pserv, Python 3.11)
                                                                 FastAPI + SQLite (app/, static/, tests/)
```

Deployment: `render.yaml` (Blueprint, Frankfurt). Knowledge graph of the repo: `graphify-out/` (refresh with `/graphify`).
`centro-de-mando_v1_respaldo/` is a frozen backup: read-only.

## 4. Stack and commands

| Part | Stack | Commands (from its folder) |
| --- | --- | --- |
| Landing + BFF | React 18, Vite 5, TypeScript, CSS Modules, Vitest; Node ≥ 20 BFF without dependencies | `npm run dev`, `npm test`, `npm run typecheck`, `npm run build` |
| Centro de mando | Python 3.11, FastAPI, SQLite, openpyxl, pytest; vanilla JS UI in `static/` | `python -m uvicorn app.main:app --port 8765`, `python -m pytest -q`, `python -m app.seed` |

New or upgraded dependencies need the owner's approval (class A). Development is on Windows 11 + PowerShell: use
`python -m uvicorn`, forward slashes in code paths, `PYTHONUTF8=1`.

## 5. Approvals

Subagents cannot ask the owner questions: they write to `docs/decisions/PENDING.md` and stop that branch of work.

- **Class A — owner approves:** new/upgraded dependencies; SQLite schema changes; scoring rules, scales, thresholds or
  minimum group size; anything touching rule zero; legal/brand wording; email senders and recipients; high-importance
  agent-file changes (tools, model, effort, permissions, scope, rules).
- **Class B — lead-architect approves and logs in `docs/decisions/DECISIONS.md`:** low-importance agent-file changes
  (wording, clarity, examples); backward-compatible API additions.
- **Class C — owning agent decides** inside its own paths and reports it.

## 6. Ownership: write only where you own

| Path | Owner |
| --- | --- |
| `CLAUDE.md`, `docs/decisions/DECISIONS.md`, `docs/contracts/` | lead-architect |
| `front-end/src/` (logic, content, api, hooks, tests) | frontend-engineer |
| `front-end/src/styles/`, `*.module.css`, `components/illustrations/`, `Logo.tsx`, `design/` | product-designer |
| `front-end/server/` | api-engineer |
| `centro-de-mando/app/` (except `db.py` schema), `centro-de-mando/static/` | api-engineer |
| `centro-de-mando/app/db.py`, `seed.py`, `data/` | database-engineer |
| `render.yaml`, `.github/`, `scripts/`, `.env.example` files | devops-engineer |
| `front-end/e2e/`, `docs/reports/qa/` | qa-engineer |
| `README.md` files, `docs/reports/`, `CHANGELOG.md` | technical-writer |
| `docs/briefs/`, `docs/proposals/` | agent-ops-engineer |

Anyone may append to `docs/decisions/PENDING.md` and `docs/HANDOFF.md`. Unit tests live next to their owner's code.

## 7. Workflow

- Branch per piece of work; never commit to `master` directly. Conventional commits (`feat(landing): …`).
- Before committing: `npm test && npm run typecheck` in `front-end/`, `python -m pytest -q` in `centro-de-mando/`.
- Backend and BFF changes are reviewed by ECC `security-reviewer`; React changes by `react-reviewer` or `typescript-reviewer`.
- Every agent ends its run with a report in `docs/reports/<agent>/<YYYY-MM-DD-HHmm>.md` (template in `docs/AGENTS.md`)
  and updates `TASKS.md`.

## 8. Definition of done

Works at 360 px and desktop, light and dark; tests and typecheck pass; rule zero respected; report written;
`TASKS.md` updated; anything blocking is in `PENDING.md`.

## 9. Model modes

Custom agents run on Claude Fable 5.2 (`model: fable`, `effort: max`). ENERGY mode forces every subagent onto Opus 5.5:
start with `scripts/start-energy.ps1` (MAX mode: `scripts/start-max.ps1`). Do not edit agent files to switch modes.
