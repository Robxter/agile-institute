# Decisions (ADRs)

## ADR-001 · 2026-11-25 · Agent architecture
Context: the owner delivered an agents package (`agents/`) written for another project (Demenova: NASA data PWA).
Decision: keep 9 agents adapted to this stack (lead-architect, frontend-engineer, product-designer, api-engineer,
database-engineer, devops-engineer, qa-engineer, technical-writer, agent-ops-engineer) as flat files in
`.claude/agents/`; discard agronomist, scientist-reviewer, data-engineer, data-scientist and instructor; move
orchestration docs to `docs/`; delete `agents/`.
Consequences: flat delegation from the main session; ownership and approvals in `CLAUDE.md`.

## ADR-002 · 2026-11-25 · Transactional email via Resend REST API
Context: the landing needs to notify the team and acknowledge pilot requests.
Decision: `front-end/server/mail.mjs` calls `POST https://api.resend.com/emails` with `fetch` (no SDK, BFF stays
dependency-free). Persist first, then send fire-and-forget with idempotency keys; without `RESEND_API_KEY` nothing is sent.
Consequences: secrets only in Render (`sync: false`); new emails reuse `sendEmail`.

## ADR-003 · 2026-11-25 · Brand mark
Decision: "Agile Institute™" (trademark) everywhere; no © in the product.
