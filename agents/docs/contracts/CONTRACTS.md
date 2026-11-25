# Demenova contracts (draft v0, to be formalised by lead-architect in phase 0)

These are the interfaces every agent builds against. lead-architect turns them into JSON Schema
(`docs/contracts/schemas/`), Pydantic (`pipeline/common/models.py`), TypeScript (`app/src/types/contracts.ts`) and
OpenAPI (`docs/contracts/openapi.yaml`). Field lists are complete for v0; values are never invented here.

## 1. Repository tree

```
/
├─ CLAUDE.md                     project rules (all agents)
├─ TASKS.md                      task board (mirrors GitHub Issues)
├─ README.md  CHANGELOG.md  .env.example  .gitignore  pyproject.toml  render.yaml
├─ .claude/
│  ├─ settings.json
│  ├─ agents/{core,backend,frontend,validation,docs}/*.md
│  └─ agent-memory/<agent>/MEMORY.md
├─ config/        datasets.yaml  alerts.yaml
├─ domain/        farm.json  practices.yaml  strategies.yaml  actions.yaml  thresholds.yaml
│                 flood_memories.yaml  glossary.yaml  tyson-answers.md  tyson-review-queue.md
├─ pipeline/
│  ├─ common/     models.py  provenance.py  grid.py  io.py
│  ├─ ingest/     imerg.py  smap.py  gldas.py  srtm.py  power.py  ecostress.py  ndvi.py  grace.py  aoi.py  __main__.py
│  ├─ engine/     terrain.py  runoff.py  travel_time.py  api_index.py  et.py  balance.py  index.py
│  │              state_machine.py  ahp.py  side_indicators.py  verification.py  snapshots.py  __main__.py
│  └─ data/       raw/ (git-ignored)  processed/
├─ backend/       app/{main.py, email.py, telegram.py, settings.py, supabase.py}  tests/
├─ supabase/      migrations/*.sql  policies/*.sql  seed/demo_farm.sql  tests/*.sql  README.md
├─ app/
│  ├─ public/     manifest.webmanifest  icons/  data/demo/...
│  └─ src/        main.tsx  App.tsx  types/  data/  state/  i18n/{en,es}.ts  units.ts
│                 screens/{Home,Map,Lot,Strategies,Alerts,Learn,Setup}/  components/  components/ui/  styles/
├─ design/        BRIEF.md  tokens.md  logo/  components/  screens/
├─ tests/         test_provenance.py  e2e/
├─ scripts/       check_provenance.py  check_bundle_size.mjs  start-max.ps1  start-energy.ps1
└─ docs/          SPEC.md  AGENTS.md  WORKFLOW.md  DATA_POLICY.md  HANDOFF.md  SI_USE_LOG.md  CITATIONS.md
                  contracts/  decisions/{DECISIONS.md,PENDING.md}  reports/  briefs/  proposals/  guide/  project-page/
```

## 2. Conventions

| Topic | Rule |
| --- | --- |
| Storage CRS | EPSG:4326 (GeoJSON) |
| Analysis grid | EPSG:32717 (UTM 17S), 30 m, aligned to the SRTM tile |
| Time | UTC ISO 8601 stored; display America/Guayaquil by default |
| Dates | `YYYY-MM-DD` in data; display DD/MM/YYYY (metric) or MM/DD/YYYY (imperial/US locale) |
| Units stored | mm (rain, water), °C, m, ha, m³/s, unitless indices; percent as 0–1 fractions |
| Units displayed | metric default; imperial toggle: in, °F, ft, acres |
| IDs | `farm_<slug>`, `lot_<farm>_<n>`, `zone_<farm>_<low|mid|high>`, ULIDs for events |
| Severity enum | `normal`, `watch`, `warning`, `severe`, `stale` |
| Origin enum | `sourced`, `calibrated`, `provided`, `observed`, `estimated`, `synthetic`, `design`, `pending` |
| Data level enum | `0` pin, `1` outline + zones, `2` lots, `3` field notes |

Every numeric field in an entity is paired with origin metadata, either as `<field>_origin` or in an `origin` map.

## 3. Entities

**Farm**: id, name, owner_id (null for demo), country, province, canton, location (Point), outline (Polygon|null),
data_level (0–3), crop, variety (+origin), catchment_id, alert_email (null|email), language (en|es),
units (metric|imperial), mode (farmer|agronomist), storage_mode (full|saver), is_demo (bool), created_at, updated_at.

**Lot**: id, farm_id, name, geometry (Polygon), area_ha (+origin), plant_age_months (+origin), variety (+origin),
drainage_class (good|moderate|poor, +origin), drainage_works (none|ditches|other, +origin), cover_crop
(none|mani_forrajero|other, +origin), last_soil_analysis {date, ph, organic_matter_pct} (+origin),
nematode_incidence (low|medium|high, +origin), disease_notes, bioinputs {mycorrhizae_last, mm_last} (+origin),
twi_mean, twi_max, twi_tercile, defined_by, to_be_redefined_by, origin.

**Zone** (data level 1): id, farm_id, tercile (low|mid|high), geometry, twi_range [min,max], origin `calibrated|sourced`.

**DailyFeature** (per lot or zone per day): unit_id, date, rain_local_mm, rain_upstream_24h_mm, _48h_mm, _72h_mm,
runoff_upstream_mm, soil_moisture (fraction|null), soil_moisture_source (smap|api|null), api_index, et0_mm, etc_mm,
balance_mm, balance_7d_mm, positive_balance_days, percentiles {upstream, saturation, local, balance},
twi_rank, temp_mean_c, rh_mean, leaf_wet_hours, heat_units, ndvi (+date of image), provenance_ids [].

**AlertState** (current per unit): unit_id, level, w, factors [{name, share}], since, updated_at,
newest_rain_data_at, confirmations (0–2), confidence (0–3), side {sigatoka: level|null, cold: level|null}.

**AlertEvent**: id, unit_id, from_level, to_level, w, factors, at, email_sent (bool), telegram_sent (bool).

**FloodMemory**: id, farm_id, date_or_month, lots_or_zone, days_with_water, damage_notes, reported_by, origin `observed`,
matched_event_id (null|engine event), created_at.

**FieldNote**: id, lot_id, kind (soil_analysis|water_table|management|other), date, value_json, origin, created_at.

**PracticeTable / Strategy** (domain files, see agronomist): practice_id, name_es, name_en, waterlogging_tolerance_days,
root_depth_cm, soil_benefits, cost_usd_ha, labour, risks, sources[], approved_by; strategy_id, lot_scope, label (A|B|C),
what, why, evidence[], benefits, gaps, risks, scores {soil, water, cost, labour}, approved_by, origin.

**EmailLog**: id, unit_id, episode_start, to_hash, provider_id, status (queued|sent|failed), created_at.

**TelegramSubscriber**: chat_id (encrypted or hashed where possible), farm_id, started_at, active.

**UserPrefs**: user_id/device_id, language, units, mode, storage_mode, theme (system|light|dark).

**Provenance**: as in `docs/DATA_POLICY.md` §3.

## 4. App data snapshots (`app/public/data/demo/`)

| File | Content | Max size |
| --- | --- | --- |
| `manifest.json` | dataset versions, provenance ids, replay window, generated_at, engine commit | 20 KB |
| `farm.json` | demo farm + lots (synthetic, labelled) | 100 KB |
| `zones.geojson` | TWI terciles | 150 KB |
| `catchment.geojson` | upstream catchment outline (simplified) | 150 KB |
| `replay/<YYYY-MM-DD>.json` | AlertState for every unit + key DailyFeature values that day | 40 KB each |
| `history/<unit_id>.json` | 90-day DailyFeature series for charts | 60 KB each |
| `strategies.json` | strategies per lot with scores and approval status | 60 KB |
| `verification.json` | events, hits, misses, false alarms, POD, FAR, CSI (counts first) | 10 KB |

Total committed demo data under 5 MB. Raw data never committed.

## 5. Config files

`config/alerts.yaml` keys (values from SPEC, each with value/origin/source-or-reason/last_changed):
weights {upstream, saturation, terrain, local, balance}; levels {watch: 0.40, warning: 0.60, severe: 0.80};
deescalate {watch: 0.30, warning: 0.50, severe: 0.70}; severe_confirmations: 2; stale_after_hours: 12;
waterlogging_days_floor_warning: 2; root_depth_cm: 70; api_k; curve_number_by_cover_soil; travel_lag_hours;
sigatoka {t_mean_c: 23, rh_mean: 0.75, rh_unfavourable: 0.70, days: 3, leaf_wet_rh: 0.90};
cold {base_c: 14, weekly_threshold_rule}.

`config/datasets.yaml`: per dataset: key, provider, short_name, version, url_opened, accessed, spatial_res,
temporal_res, latency, variables, use_in_demenova, verified_by.

## 6. Backend API (FastAPI; nothing user-facing depends on it)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | none | liveness |
| POST | `/run` | `X-Admin-Token` | trigger pipeline+engine run for a farm or all |
| POST | `/email/test` | `X-Admin-Token` | send a test Severe email to the configured inbox |
| POST | `/telegram/webhook` | Telegram secret-token header | `/start <farm_code>`, `/estado` |

Environment: see `.env.example`.

## 7. Identity and storage (ADR-003, ADR-004)

- Device identity: Supabase anonymous sign-in on first launch; farms created on the device belong to that user.
  If sign-in is unavailable, the app runs local-only and says so. No email/password login in v0.
- Storage modes: Full = status + 90 days history + imagery tiles cache; Data saver = status + 7 days, no imagery cache.
  User-created farms persist in IndexedDB and sync to Supabase when online.
