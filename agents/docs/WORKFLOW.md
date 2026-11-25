# Demenova workflow: from empty repo to submission

All times are Spain time (CET). Deadline 15 Nov 23:59; target submission 20:00. Roster sleeps about 00:00 to 04:30.
Every prompt below is meant to be pasted into the **main Claude Code session** as written.

---

## Step 0. Accounts and tools (Roster, about 25 min, can overlap with phase 0)

| Item | Action | Done |
| --- | --- | --- |
| NASA Earthdata | Create account at urs.earthdata.nasa.gov; approve the GES DISC application when first downloading | [ ] |
| Supabase | Create project (closest US region); enable anonymous sign-ins in Authentication settings | [ ] |
| Render | Sign in with GitHub; do not create services yet (devops-engineer writes render.yaml) | [ ] |
| Resend | Create account and API key; sending without a domain reaches only your own inbox (fine for the demo) | [ ] |
| Telegram | In Telegram, message @BotFather, `/newbot`, name "Demenova", username like `DemenovaBot`; keep the token | [ ] |
| uv | PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | [ ] |
| frontend-design | In Claude Code: `/plugin install frontend-design@claude-plugins-official`, then `/reload-plugins` | [ ] |
| ECC, Graphify | Already installed. Check ECC rules: `.claude/rules/ecc/common`, `python`, `typescript` exist | [ ] |

## Step 1. Install this kit into the repo (10 min)

```powershell
cd $HOME
git clone https://github.com/Robxter/NASA-Space-Apps-Demenova.git
cd NASA-Space-Apps-Demenova
# Unzip the kit here so CLAUDE.md sits at the repo root and .claude\ merges with any existing one.
Expand-Archive -Path "$HOME\Downloads\demenova-claude-kit.zip" -DestinationPath . -Force
Copy-Item .env.example .env   # then fill .env in VS Code; never commit it
```

1. Open the Claude Doc "Demenova — Project Specification", download it as Markdown, save as `docs/SPEC.md`.
2. Check `domain/tyson-answers.md` (already filled with Tyson's answers so far). Paste new answers there as they come.
3. Commit:

```powershell
git checkout -b block/0-skeleton
git add .
git commit -m "chore: add Demenova agent kit, spec and data policy"
git push -u origin block/0-skeleton
```

## Step 2. Start the orchestrator session

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-max.ps1
```

Accept the workspace-trust dialog (needed for project agents' settings). Then paste:

```text
Read CLAUDE.md, docs/AGENTS.md and docs/WORKFLOW.md. You are the orchestrator. List the 14 custom agents
you can delegate to with their model and effort, confirm ECC's planner and reviewers are available, and
confirm that every subagent will load CLAUDE.md. Do not start any work yet.
```

If an agent is missing, restart Claude Code once (a new `.claude/agents` directory needs a restart).

---

## Phase 0. Skeleton (lead-architect, about 45 min)

```text
@lead-architect Run your Phase 0 deliverable exactly as defined in your agent file, using
docs/contracts/CONTRACTS.md as the draft. Create the tree, schemas, models, types, OpenAPI sketch, config stubs
with null values, scripts/check_provenance.py with its test, ADR-001 to ADR-004, empty DECISIONS.md and
PENDING.md, and TASKS.md phase 1 items per agent. Add no dependency beyond CLAUDE.md §4. Report when done.
```

Then:

```text
Run /code-review on the phase 0 changes, then run the provenance test and the empty app build. Summarise
PENDING.md for me. If green, commit on block/0-skeleton with message "feat(skeleton): phase 0", push, and
open a PR to main.
```

Optional: `/graphify .` now that a skeleton exists.

## Phase 1. Foundations in parallel (about 2 h)

Paste as one message; these agents own disjoint paths and can run in the background together:

```text
Create branch block/1-foundations from main after merging phase 0. Then run in parallel:
1. @data-engineer: verify every dataset in config/datasets.yaml against official pages, build the AOI for
   the Pasaje/Buenavista demo area, delineate the upstream catchment from SRTM, generate the synthetic demo
   lot geometry, download IMERG daily history 2015-01-01 to today for the catchment, and build the replay
   stack for 2026-02-15 to 2026-03-05. List the top 15 heaviest 72-hour upstream rain events with dates.
2. @database-engineer: write the schema, RLS and views as migrations, plus RLS tests. Do not apply them;
   put the SQL diff in PENDING.md for my approval.
3. @product-designer: write design/BRIEF.md with the revised token plan, three logo options, the severity
   palette for light and dark, and the presentational components with their specs.
4. @agronomist: build domain/ files from the SPEC and domain/tyson-answers.md, queue everything unapproved in
   domain/tyson-review-queue.md in Spanish, and save the memory note about Tyson redefining the demo lots.
When all four finish, show me their reports' "Open issues" and every PENDING.md item, with your
recommendation for each.
```

**Checkpoint A (Roster, 10 min):** approve or change the schema SQL, pick a logo, answer any dependency request.
Paste the 15 flood candidates to Tyson. Then:

```text
Apply the approved schema to Supabase using the instructions in supabase/README.md (I will run the SQL in
the Supabase SQL editor if you tell me exactly what to paste). Then run technical-writer for the block 1
report, commit, push and open a PR.
```

## Phase 2. Engine, app shell, email (about 3 h)

```text
Create branch block/2-core. Run:
1. @data-scientist: build the engine in your agent file's order on the replay window, with tests, the
   calibrated travel lag from the 22-23 Feb 2026 event, verification counts for the documented floods, and
   the replay snapshots in app/public/data/demo/. Weights stay the SPEC starting weights tagged estimated.
2. In parallel @frontend-engineer: app shell, hash navigation, data layer (Supabase, snapshots, IndexedDB),
   replay scrubber, Home, Map, Lot detail, units and language toggles, using product-designer's components.
3. In parallel @api-engineer: FastAPI with /health, /run, /email/test and the Severe email with dedupe.
When data-scientist finishes, run @scientist-reviewer on pipeline/engine and config/alerts.yaml, and ECC
code-reviewer on the same diff. Turn blockers into TASKS.md items for the owner and fix them before merging.
```

## Before Roster sleeps (about 23:30)

```text
1. @devops-engineer: CI, pipeline workflow (manual run once), render.yaml, deploy the app as a Render
   Static Site and the backend as a Web Service, size-budget gate. Record live URLs in HANDOFF.md.
2. @technical-writer: block 2 report and SI-use log entries for everything today.
3. Write a HANDOFF.md entry for Tyson's night shift (Spanish summary): preview link, DEVICE_CHECKLIST items
   for the Galaxy A55, tyson-review-queue.md items, project page draft location.
4. Commit and push; then /save-session.
```

Tyson works overnight from his doc and the preview (no code). Optional for long unattended reviews: restart with
`scripts\start-energy.ps1` to save usage; Fable is the default for building.

## Day 2, 04:30 to 15:00: complete the scope

```text
/resume-session. Read HANDOFF.md, Tyson's answers (I pasted them into domain/tyson-answers.md) and the
GitHub issues he opened. Create branch block/3-scope. Then:
1. @agronomist: replace every estimated value Tyson answered; mark approved items; keep the rest queued.
2. If Tyson sent his AHP pairwise matrix: @data-scientist compute weights and CR; if CR <= 0.10 put the new
   weights in PENDING.md for my approval; regenerate snapshots after I approve.
3. @frontend-engineer: Strategies screen, Alerts screen, Learn, Farm setup with data levels 0-3, farmer/
   agronomist mode, data saver, fixes from Tyson's issues.
4. @api-engineer: Telegram bot if email is done.
5. @qa-demo-engineer: e2e suite and the replay acceptance test; write DEVICE_CHECKLIST.md.
6. @instructor: guides and judge quick start.
Show me failures and PENDING items as they appear.
```

Nice-to-haves only if everything above is green, in the SPEC cut order (reverse): language toggle, mode toggle,
flood memory, level 3 notes, Telegram, priority sliders, Costa Rica map, live polling, spraying indicator.

## 15:00 Feature freeze

```text
Feature freeze. Run: qa-demo-engineer full suite; scientist-reviewer final review of engine, guides and
project page claims; ECC security-reviewer on backend and app; provenance checker; size gate. Fix only
blockers. Then @technical-writer: final README, CITATIONS.md, CHANGELOG, SI-use description and the
project page in English, plus a Spanish summary for Tyson. Merge to main and tag v1.0.0.
```

## 15:00 to 19:00 Demo video (humans, with Claude's help)

30 seconds, English or Spanish with English subtitles: 5 s problem (Tyson), 20 s replay (rain upstream → lot turns
Severe → email arrives → water reaches the farm), 5 s strategies + "From orbit to the root zone." No NASA logo.
Host it publicly (the Space Apps site does not host videos) and test the link in a logged-out browser window.

## 19:00 to 20:00 Submit

Checklist: all members on the Members tab; every required field in English; demo link public; SI-use description;
data citations; no minors' likeness; press Submit (not just save). Buffer until 23:59.

---

## Energy mode: when to use it

Use `scripts\start-energy.ps1` (Opus 5.5 for everything) for long review sweeps, documentation passes and overnight
or repetitive runs. Use MAX mode (Fable 5.2) for phase 0, the engine, scientific review and design work.

## If something goes wrong

| Symptom | Do |
| --- | --- |
| Agent not found | Restart Claude Code; run `claude plugin validate .claude/agents` |
| Effort warning | Note it; agent-ops-engineer proposes `xhigh` for that agent |
| Build broken | `/build-fix` |
| Context getting slow | `/context-budget`, then `/save-session` and start a fresh session with `/resume-session` |
| Earthdata download denied | Approve the provider's application in your Earthdata profile, retry |
| Supabase anonymous sign-in fails | Check it is enabled in Authentication settings; the app keeps working locally |
| Usage limits approaching | Switch to energy mode |
