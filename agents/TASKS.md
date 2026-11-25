# Demenova tasks

Mirrors GitHub Issues (one issue per task ID; label = agent, milestone = block). The main session keeps both in sync;
if the GitHub CLI is installed and authenticated, it may run `gh issue create --title "T-001 ..." --label <agent>`.
Status: [ ] todo, [~] in progress, [x] done, [!] blocked (see PENDING.md).

## Block 0: skeleton
- [ ] T-001 lead-architect: repo tree and folder READMEs
- [ ] T-002 lead-architect: JSON Schemas, Pydantic models, TS types, OpenAPI sketch from CONTRACTS.md
- [ ] T-003 lead-architect: config stubs (datasets.yaml, alerts.yaml) with null values and origins
- [ ] T-004 lead-architect: scripts/check_provenance.py + tests/test_provenance.py
- [ ] T-005 lead-architect: ADR-001..004, DECISIONS.md, PENDING.md, HANDOFF.md
- [ ] T-006 Roster: accounts (Earthdata, Supabase + anonymous sign-in, Render, Resend, Telegram bot), .env filled

## Block 1: foundations
- [ ] T-010 data-engineer: verify datasets and fill config/datasets.yaml with URLs and access dates
- [ ] T-011 data-engineer: AOI Pasaje/Buenavista, SRTM catchment delineation
- [ ] T-012 data-engineer: synthetic demo lot geometry (8 lots, 5–7 ha, low and high TWI)
- [ ] T-013 data-engineer: IMERG daily 2015→today for catchment; top-15 72 h events list
- [ ] T-014 data-engineer: harmonized replay stack 2026-02-15 → 2026-03-05 (IMERG, SMAP/GLDAS, POWER, NDVI)
- [ ] T-015 database-engineer: migrations, RLS, views, RLS tests (class A before applying)
- [ ] T-016 product-designer: BRIEF.md, three logos, severity palette, tokens, ui components
- [ ] T-017 agronomist: domain files; tyson-review-queue.md (Spanish); memory note on demo lots
- [ ] T-018 Roster: checkpoint A (schema, logo, dependencies); send flood candidates to Tyson

## Block 2: core
- [ ] T-020 data-scientist: terrain features, TWI terciles, zones
- [ ] T-021 data-scientist: runoff (CN), Kirpich first lag, calibrated lag on Feb 2026 event
- [ ] T-022 data-scientist: API, FAO-56 ETc, daily balance, 2-day floor rule
- [ ] T-023 data-scientist: index W, state machine, side indicators, explanations, confidence
- [ ] T-024 data-scientist: verification counts; replay snapshots; tests
- [ ] T-025 scientist-reviewer + code-reviewer: engine review; blockers → tasks
- [ ] T-026 frontend-engineer: shell, navigation, data layer, IndexedDB, replay scrubber
- [ ] T-027 frontend-engineer: Home, Map, Lot detail; units and language toggles
- [ ] T-028 api-engineer: FastAPI health/run/email-test; Severe email with dedupe; tests
- [ ] T-029 devops-engineer: CI, pipeline workflow, render.yaml, deploys, size gate
- [ ] T-030 technical-writer: block 2 report, SI-use log; HANDOFF for Tyson's night shift

## Block 3: scope completion (day 2)
- [ ] T-040 agronomist: apply Tyson's answers; approvals; remaining queue
- [ ] T-041 data-scientist: AHP weights from Tyson's matrix (class A to apply)
- [ ] T-042 frontend-engineer: Strategies, Alerts, Learn, Farm setup data levels 0–3, modes, data saver
- [ ] T-043 api-engineer: Telegram bot (nice-to-have)
- [ ] T-044 qa-demo-engineer: e2e suite, replay acceptance, DEVICE_CHECKLIST.md
- [ ] T-045 instructor: farmer and agronomist guides (es/en), judge quick start, Learn cards
- [ ] T-046 Tyson: device checklist on Galaxy A55; issues; project page draft; video script and voice

## Freeze and submission (day 2, 15:00 → 20:00)
- [ ] T-050 qa + scientist-reviewer + security-reviewer final pass; provenance and size gates
- [ ] T-051 technical-writer: README, CITATIONS, CHANGELOG, SI-use description, project page (en) + Tyson summary
- [ ] T-052 Roster + Tyson: 30-second video with English subtitles, public link
- [ ] T-053 Roster: submit by 20:00 Spain; confirm all members and public links

## Waiting on Tyson (questionnaire 5.1–5.10, Tasks 5–7 in his doc)
- [ ] T-060 variety, density, soil type, drainage depth/spacing
- [ ] T-061 actions per alert level; solo-farmer actions; local vocabulary; preferred channel
- [ ] T-062 biosecurity text (Fusarium TR4) — nothing shown until approved
- [ ] T-063 evidence of zero-data farms; flood memory table; AHP pairwise comparisons
- [ ] T-064 redefine the demo farm's imaginary lot layout and attributes
