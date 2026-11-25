# Agile Institute™ agent system

9 custom agents in `.claude/agents/`, plus ECC reviewers, coordinated by the **main Claude Code session** (the
orchestrator) under the owner's direction. Adapted from the agents package delivered in `agents/` (2026-11-25):
agents that only made sense for that project (agronomist, scientist-reviewer, data-engineer, data-scientist,
instructor) were discarded.

## 1. Roster

| # | Agent | Owns | Writes code? | Memory |
| --- | --- | --- | --- | --- |
| 1 | lead-architect | `CLAUDE.md`, contracts, ADRs, class B approvals | Contracts only | project |
| 2 | frontend-engineer | Landing logic, content, API client, Vitest | Yes | none |
| 3 | product-designer | Tokens, CSS Modules, logo, illustrations, visual polish | Yes (styles) | project |
| 4 | api-engineer | Node BFF, Resend email, FastAPI endpoints, centro de mando UI logic | Yes | none |
| 5 | database-engineer | SQLite schema, seed/DEMO data, importer integrity | Yes | none |
| 6 | devops-engineer | `render.yaml`, CI, scripts, env var map | Yes | none |
| 7 | qa-engineer | Playwright e2e, accessibility and performance checks | Tests only | none |
| 8 | technical-writer | READMEs, changelog, block reports | Docs | project |
| 9 | agent-ops-engineer | Briefs from vague requests, agent audits, proposals | Briefs only | project |

**ECC agents reused** (by their ECC names): `planner` (`/ecc:plan`), `code-reviewer`, `security-reviewer`,
`react-reviewer`, `typescript-reviewer`, `python-reviewer`, `fastapi-reviewer`, `database-reviewer`, `a11y-architect`,
`build-error-resolver` (`/build-fix`), `e2e-runner`. Custom names never reuse an ECC name.

**Skills worth loading:** `frontend-design`, `web-design-guidelines`, `ecc:accessibility`, `ecc:react-performance`,
`ecc:vite-patterns`, `ecc:fastapi-patterns`, `ecc:deployment-patterns`, `graphify`, and the project skill
`frontend-optimize` (`.claude/skills/frontend-optimize/`).

## 2. Models and effort

- MAX mode (default, `scripts/start-max.ps1`): custom agents use `model: fable` and `effort: max`.
- ENERGY mode (`scripts/start-energy.ps1`): `CLAUDE_CODE_SUBAGENT_MODEL=opus` + `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`,
  every subagent on Opus 5.5. Agent files are never edited to switch modes.

## 3. Orchestration protocol (main session)

Delegation is flat (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`): main session → agent, never agent → agent.

1. Read `CHANGES.md`, `TASKS.md`, `docs/HANDOFF.md`, `docs/decisions/PENDING.md`.
2. For anything larger than a few files, run `/ecc:plan` and show the plan to the owner.
3. Launch agents per §5; agents with disjoint owned paths may run in parallel.
4. When an agent finishes: read its report; turn blockers into `TASKS.md` items; route reviews
   (BFF/backend → security-reviewer; React → react-reviewer; schema → database-reviewer).
5. Ask the owner every class A question from PENDING.md in one batch, with options and a recommendation.
6. Update `docs/HANDOFF.md`; commit on the work branch.

## 4. Approval flow

| Class | What | Who approves | How |
| --- | --- | --- | --- |
| A | Dependencies, schema, scoring rules and thresholds, rule zero, legal/brand wording, email senders/recipients, high-importance agent-file changes | Owner | PENDING.md entry; agent stops that branch; main session asks |
| B | Low-importance agent-file changes; backward-compatible API additions | lead-architect | Applied and logged in DECISIONS.md |
| C | Anything else inside an agent's own paths | Owning agent | Reported in its run report |

Agent-file change path: agent-ops-engineer proposal → lead-architect → class B applied / class A to the owner.

## 5. Routing: who does what

| Request | Agent(s), in order |
| --- | --- |
| Landing copy, sections, behaviour | frontend-engineer (+ product-designer for look) → qa-engineer |
| "Make it look better / less generic" | agent-ops-engineer (brief) → product-designer → frontend-engineer → qa-engineer |
| Frontend performance / accessibility | product-designer + frontend-engineer with `/frontend-optimize` → qa-engineer |
| Email (Resend) or BFF endpoint | api-engineer → security-reviewer |
| Centro de mando endpoint or dashboard | api-engineer (+ database-engineer if data) → python-reviewer/fastapi-reviewer |
| Schema or seed change | database-engineer → database-reviewer → owner (class A) |
| Deploy / Render / CI | devops-engineer (or `/build-fix`) |
| README, changelog, report | technical-writer |
| Knowledge graph refresh | main session: `/graphify` (update mode) |
| "An agent keeps doing X wrong" | agent-ops-engineer (audit + proposal) → lead-architect |

## 6. Report template (every agent, every run)

File: `docs/reports/<agent>/<YYYY-MM-DD-HHmm>.md`

```markdown
# <agent> report <YYYY-MM-DD HH:mm Spain>
Model/effort: <fable max | opus ...>   Task IDs: <T-...>   Branch: <...>
## Done
- <change> (<files>) (<commit>)
## Data and claims
- New values or copy introduced and their source (scoring | workbook | DEMO | illustrative | pending)
## Tests and checks
- <command> → <result>
## Decisions
- Class C taken: ...   Class A/B raised: <PENDING.md / proposal id>
## Open issues and risks
## Next steps
```

## 7. Handoff template (`docs/HANDOFF.md`, newest entry on top)

```markdown
## <YYYY-MM-DD HH:mm Spain> - <from> to <to>
State: <one sentence>
Done since last handoff: ...
Waiting on owner: <PENDING ids>
Next, in order: 1. ... 2. ...
Do not touch: ...
```
