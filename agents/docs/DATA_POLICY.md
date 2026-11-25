# Data policy: NO INVENTED DATA

This is Demenova's first rule and it outranks speed, aesthetics and deadlines. A demo that shows one invented number
loses the trust the whole project is built on. Every agent reads this file before producing any value.

## 1. The six legitimate origins

Every stored or displayed value carries exactly one `origin`:

| origin | Meaning | Required metadata | UI treatment |
| --- | --- | --- | --- |
| `sourced` | Read from a dataset or publication someone opened | provenance id or source URL + access date | Source tooltip |
| `calibrated` | Fitted on documented events with recorded evidence | calibration note id | Source tooltip |
| `provided` | Typed or imported by a user | user id or device id, timestamp | "Provided" badge |
| `observed` | A field observation (water table reading, flood memory) | observer, date | "Observed" badge |
| `estimated` | Expert or literature default awaiting confirmation | `estimated_by`, `reason`, TASKS id | "Estimated" badge |
| `synthetic` | Demo-only invented content (Finca Demo El Oro) | `to_be_redefined_by` | Visible "Demo" label |

`design` is reserved for engineering parameters (hysteresis, two-update rule, 12 h Stale) and `pending` for values
that do not exist yet (they are `null` in data and shown as missing).

## 2. Hard rules

1. No value without an origin. The provenance checker (`scripts/check_provenance.py`) fails the build otherwise.
2. Missing stays missing. Show "No data" with the reason. No silent interpolation, smoothing or forward-fill.
   The only gap-filling allowed is a method in the SPEC's Prediction science table, and its output is `estimated`.
3. Synthetic data appears only in the demo farm and only with the visible "Demo" label. It never enters
   calibration or verification.
4. No fabricated citations. A source is cited only after an agent opened it; record URL and access date.
   If verification fails, write `UNVERIFIED`, do not use the value, and add a PENDING.md entry.
5. No unmeasured claims. Accuracy language ("accurate", "predicts", "validated") needs measured verification counts.
   Use "caught the February 2026 flood in replay" (true, measured) rather than "95% accurate" (invented).
6. Language models are not data sources. An agent's general knowledge may suggest where to look; the value must
   still come from an opened source.
7. When in doubt, stop and write to `docs/decisions/PENDING.md`. Stopping is success; inventing is failure.

## 3. Provenance record (attached to every data file)

```json
{
  "provenance": {
    "id": "prov-imerg-final-2026-02",
    "dataset": "<exact product short name>",
    "version": "<exact version>",
    "provider": "<e.g. NASA GES DISC>",
    "url": "<landing page or DOI actually opened>",
    "accessed": "2026-11-14T18:30:00Z",
    "spatial_resolution": "<as published>",
    "temporal_resolution": "<as published>",
    "aoi": "<aoi id>",
    "time_range": ["2026-02-15", "2026-03-05"],
    "processing": ["subset to AOI", "reproject EPSG:32717 30 m (method: ...)", "..."],
    "code_commit": "<git sha>",
    "agent": "data-engineer",
    "notes": ""
  }
}
```

## 4. Values awaiting Tyson (currently `estimated`)

Questionnaire 5.1–5.10 defaults: banana variety (Cavendish Williams), planting density, soil type (loam), drain depth
and spacing, actions per alert level, local vocabulary, preferred channel, biosecurity text (none until approved),
solo-farmer actions. Also: Sigatoka Watch after 3 days, cold-stress threshold, alert weights (until his AHP matrix).
Each is listed in `domain/tyson-review-queue.md` and replaced when he answers.

## 5. Already confirmed by Tyson (`origin: sourced`, source "Tyson, 14 Nov 2026")

Banana tolerates at most 2 days of waterlogging; roots at 70 cm; Machala/El Oro is the right area; his family farm
keeps no records and does not use maní forrajero; his test phone is a Samsung Galaxy A55.
