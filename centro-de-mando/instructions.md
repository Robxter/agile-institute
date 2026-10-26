# Cuadros de mando por dimensión: how the system works (v2)

This guide explains the redesigned command center built from the `Mejora/` folder.
On-screen labels are quoted in Spanish exactly as they appear in the app.

Instead of one operational dashboard, there is now one dashboard per professional dimension:
"Persona", "Equipo", "Liderazgo", "Organización", "IA transversal", and two mixed ones, "Persona + IA" and "Líder + IA".
The previous version is kept unchanged in `../centro-de-mando_v1_respaldo/`.

---

## 1. Starting the app

Run these commands from the `centro-de-mando` folder in PowerShell:

```
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8765
```

Then open http://127.0.0.1:8765.

- Use `python -m uvicorn`, not plain `uvicorn`, which is not on the PATH on this machine.
- If `data/centro_mando.db` does not exist, the server builds it on first start.
- To reset the demo data, run `python -m app.seed` and restart the server.
- To run the automated checks, run `python -m pytest -q`.

---

## 2. Where the data comes from

```
Mejora/Agile_Competences_5_Cuadros_Diseno.xlsx ──► catalog (app/catalog.py)
                                                       │
  DEMO generator (app/seed.py) ─┐                      │
  Excel import (app/importer.py)┴─► SQLite ──► quality control + scoring (app/scoring.py)
                                                       │
                              dashboards + permissions (app/dashboard.py)
                                   │                        │
                            web API (app/main.py)     Excel export (app/export_xlsx.py)
                                   │
                            browser UI (static/)
```

### 2.1 The catalog

The five questionnaires and the pulse are read from the design workbook:

| Sheet | Content |
|---|---|
| `Items_T01` | Persona · Agilidad personal (24 active items, plus 4 inactive reserves) |
| `Items_T02` | Equipo · Contribución individual al equipo |
| `Items_T03` | Liderazgo · Autopercepción de liderazgo |
| `Items_T04` | Organización |
| `Items_T05` | IA transversal (numeric 1–5 scale; verbal anchors still pending) |
| `Items_PULSO` | 12 pulse items: F01–F08, ENPS, and L01–L03 about the person's manager |

Each questionnaire has 8 competencies of 3 items. The short competency labels come from rows 61–68 of each `CM_*` sheet.

### 2.2 Capture format

Each answer row follows the `Datos_T01…T05` layout: `evaluacion_id, persona_id, organizacion_id, equipo_id, periodo, tipo_datos, fecha_iso`, then one column per item.
The pulse (`Datos_PULSO`) also has `responsable_id`.
Answers are integers 1–5 (0–10 for ENPS), `NV` for "no observable", or blank for omitted.
Identifiers are anonymous; no names or emails of participants are stored.

### 2.3 Rules

These reproduce the blue formula columns of the design workbook:

| Step | Rule |
|---|---|
| Quality control | `METADATOS` if a required field is missing or the type is not REAL/DEMO; `DUPLICADO` if the `evaluacion_id`, or the same person + period + type, appears twice; `VALOR_INVALIDO` if an answer is out of range; otherwise `OK`. Only OK rows count. |
| Competency | Mean of the valid items when at least 2 of 3 are valid. |
| Descriptive mean | Mean of the calculated competencies when at least 6 of 8 exist. |
| Group minimum | 5 people. Below it, the value is hidden and shows "Oculto" or "Muestra insuficiente". |
| Individual view | Minimum 1, but only for the person themself, administration and consultants. |
| Pulse | Each indicator is shown separately. There is no global Flow or wellbeing index. |
| eNPS | 100 × (promoters 9–10 − detractors 0–6) / valid answers, always with a minimum of 5. |
| Evolution | Only between periods with the same questionnaire version and enough sample. |

There are no norms and no A1–A5 levels. Strengths and areas are relative positions inside the profile, not diagnoses.

---

## 3. Logging in and roles

The login screen lists one demo account per role. Click one to enter; click "Salir" to switch.
Permissions are enforced on the server, so a hand-written request outside your scope is refused.

| Account | Role | What it sees |
|---|---|---|
| admin@agileinstitute.es | Administración | All seven dashboards, any person, item-level export, import, audit. |
| consultor@agileinstitute.es | Consultor | All seven dashboards for Demo Corp, any person there. |
| rrhh@democorp.demo | RRHH · solo lectura | All seven dashboards for Demo Corp, aggregates only. Can edit the organizational plan. |
| lider@democorp.demo | Líder | Own results (DC-PRO-01) in Persona, Persona + IA, Liderazgo, Líder + IA; own team in Equipo and IA. |
| participante@democorp.demo | Participante | Own results (DC-PRO-03) in Persona and Persona + IA. |
| gestor@agileinstitute.es | Gestor de test | No dashboards. |

Locked filters are shown greyed out.

---

## 4. The screens

### 4.1 Inicio

One card per dashboard you can open, with the mean and n of each questionnaire for the chosen data type and period.
Administration also sees "Importar capturas" and a link to the audit log.

### 4.2 Common parts of every dashboard

- **Header and meta strip**: questionnaire and version, period, person or "Agregado", n per questionnaire, and the group minimum.
- **Filters**: "Datos" (DEMO or REAL, never mixed), "Periodo", "Organización", "Equipo" and, in individual dashboards, "Persona" or "Líder". "Todas (agregado)" shows the group view.
- **Notice**: what this dashboard can and cannot claim.
- **KPI tiles**: four headline figures specific to the dashboard.
- **Competencies**: bars on the 1–5 scale. "Ver tabla" shows n, coverage and standard deviation.
- **Fortalezas / Áreas para explorar**: the highest and lowest competencies of the profile.
- **Plan de desarrollo**: an objective plus actions at 30, 60 and 90 days, with owner, date, state and evidence. It is saved per dashboard and selection, and audited.
- **Pulse panels**, **Evolución** and **Sobre los datos** (quality control of the cut; in an individual view, only that person's own captures).

### 4.3 Customizing the layout

Click "Personalizar" to enter edit mode. Every KPI tile and panel gets a toolbar:

- Drag the ⠿ handle to move the tile, with a mouse or by touch. Dragging near the top or bottom edge scrolls the page. With the keyboard, focus the handle and press the arrow keys.
- Use − and + to change the width: ¼, ⅓, ½, ⅔, ¾ or "completo" (full width).
- Use the eye button to hide or show the tile. Hidden tiles stay visible, dimmed, while you edit.

Then click "Guardar distribución", "Cancelar", or "Volver a la distribución estándar".
Outside edit mode, a "Distribución estándar" button appears whenever the dashboard has a saved custom layout.

The layout is saved per user and per dashboard, and it applies to every filter.
On medium screens narrow tiles widen, and on phones every tile is full width, so the width buttons are hidden there.
Customizing changes only the presentation, never which data a role may see.

### 4.4 Dashboard-specific panels

| Dashboard | Specific panels |
|---|---|
| Persona | Radar profile; "Mis respuestas por competencia" (each circle is an item, the diamond is the competency mean); scale legend. |
| Equipo | "Media y acuerdo del equipo" (mean vs. standard deviation, numbered points); "Cómo responde el equipo" heat map; team eNPS; organization mean as a reference mark on the bars; participation dots. |
| Liderazgo | "Lo que percibe mi equipo" (L01–L03 from the leader's direct reports); "Conversaciones para abrir" and "Lo que más practicas"; "Fuentes y muestra". No gap is computed, because L01–L03 are different questions. |
| Organización | Eight competency cards; eNPS donut; results by team (teams under 5 hidden); the five profiles, each with its own n; three priorities. |
| IA transversal | IA by team; most and least frequent behaviours (items with at least 5 answers); IA radar. |
| Persona + IA | T01 (blue) and T05 (orange) side by side; "puentes de lectura" chart pairing related competencies; combined strengths and areas tagged by questionnaire. |
| Líder + IA | T03 and T05 side by side; the leader's T05 bars carry a mark for "IA de mi equipo" (T05 of the leader's reports, minimum 5); leader–IA bridges; perception received. In the aggregate view it compares leaders' T05 with everyone else's. |

Every chart has tooltips on hover or keyboard focus, and most have a "Ver tabla" view. Dark mode follows the system setting, and the layout adapts to phones.

---

## 5. Excel

"Descargar Excel" exports the dashboard with the filters on screen:

| Sheet | Content |
|---|---|
| Cuadro | KPIs, competency table and native bar chart per questionnaire, strengths and areas. |
| Pulso | Each pulse indicator and the eNPS breakdown. |
| Detalle | Dashboard-specific tables (teams, five profiles, bridges, behaviours, perception received, distribution). |
| Trazabilidad | Who exported, filters, versions, minimums, rules and quality control. |
| Datos_Txx | Administration only, with a reason of at least 10 characters: rows in the capture format, item by item. |

Every export is recorded in the audit log.

## 6. Importing REAL data

1. Fill in `Datos_T01…T05` and `Datos_PULSO` in a copy of the design workbook, with `tipo_datos = REAL`.
2. In "Inicio", as administration, use "Importar capturas", or run `python -m app.importer RUTA.xlsx`.
3. Choose "Datos: REAL" and the period in any dashboard.

A row whose `evaluacion_id` already exists replaces the previous one. Repeated ids inside the same file are flagged as `DUPLICADO`.
Unknown organizations, teams and people are created with their anonymous ids. Leaders are inferred from `responsable_id` in the pulse.

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn` is not recognized | Run `python -m uvicorn app.main:app --port 8765`. |
| The port is in use | Stop the other copy or use `--port 8766`. |
| A panel says "Muestra insuficiente" or "Oculto" | The group has fewer than 5 people. This is by design. |
| "Esta es la línea base" in Evolución | Only one comparable period has enough data. |
| A role sees less than expected | Check the role table in section 3. |
| The data looks stale | Run `python -m app.seed`, then restart the server. |
