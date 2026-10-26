   # Centro de mando: how the system works

This guide explains what the Centro de mando does, how its data flows, and how each part of the screen and the Excel download works.
On-screen labels are quoted in Spanish exactly as they appear in the app.

The Centro de mando is menu 5, "Informes y cuadros de mando", of the Centro de Test MVP.
It is specified in section 7 of `Resources/Documento_Funcional_MVP_Centro_de_Test_v1_0`.
Its job is aggregated analytics: how many tests were sent, how many were completed, how people scored, and a downloadable Excel of all that.
It is not the archive of individual reports. That is menu 3, "Informes", which is a different module.

---

## 1. Starting the app

Run these commands from the `centro-de-mando` folder in PowerShell:

```
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8765
```

Then open http://127.0.0.1:8765.

- Use `python -m uvicorn`, not plain `uvicorn`. On this machine the plain command is not on the PATH.
- If the database file `data/centro_test.db` does not exist, the server builds it automatically on first start.
- To stop the server, press Ctrl+C in the window where it runs.
- Only one copy can run on port 8765 at a time. If the port is busy, stop the other copy or use `--port 8766`.

### Resetting the demo data

```
python -m app.seed
```

This deletes the database and rebuilds it from the Excel master.
The fictitious activity is generated relative to today's date, so "pending" and "expired" stay realistic whenever you reset.
Restart the server afterwards so it picks up the new database.

### Running the tests

```
python -m pytest -q
```

---

## 2. How the data flows

```
Excel master  ──►  importer (app/seed.py)  ──►  SQLite database (data/centro_test.db)
                                                   │
                       scoring engine (app/scoring.py) computes results on completion
                                                   │
                 analytics + permissions (app/dashboard.py)
                        │                                   │
              web API (app/main.py)                Excel export (app/export_xlsx.py)
                        │
              browser UI (static/index.html, app.js, styles.css)
```

### 2.1 The Excel master is the source of truth for the catalogue

The importer reads `Resources/Excel_Maestro_Importable_Centro_de_Test_MVP_v1_0.xlsx`.
It follows the sheet order in the `MAPA_IMPORTACION` sheet.

| Excel sheet | What it becomes |
|---|---|
| `USUARIOS` | Companies and people. The email is unique, and an existing person is updated, not duplicated. |
| `TESTS` | The test catalogue: code, name, version, expiry days and reminder days. |
| `FICHAS_TECNICAS` | Used to detect tests that have a technical sheet but are missing from `TESTS`. |
| `INDICADORES` | The indicators of each test, with their order, weight and score range. |
| `ITEMS` | The questions, each linked to one indicator, with a flag for reverse scoring. |
| `OPCIONES_RESPUESTA` | The answer scales, for example LIKERT5 with values 1 to 5. |
| `REGLAS_PUNTUACION` | How to score: indicator mean, weighted global mean, rounding and scoring version. |
| `INTERPRETACIONES` | Score ranges and level names, such as Inicial, En desarrollo, Competente, Avanzado and Referente. |

While importing, it prints warnings about problems it finds in the Excel, for example a test without a code.
Rows it cannot use safely are skipped rather than guessed. The README lists the current warnings.

### 2.2 Demo activity is fictitious

The Excel contains no real sends or answers, so the importer generates fictitious ones.
It creates extra demo people, invitations, answers, reminder emails and completion emails across three demo companies.
It also creates four staff accounts, one per role.
Section 15 of the functional document requires fictitious data before the pilot.
No real personal data is ever created.

Every completed demo invitation is scored by the real scoring engine, never by made-up numbers.

### 2.3 The scoring engine

Scoring follows the rule in the document: compute first, then interpret, and never the reverse.

1. **Reverse items.** Items marked `reverse_scored` are flipped before anything else. On a 1 to 5 scale, an answer of 2 becomes 4. The general rule is the scale's minimum plus its maximum, minus the answer.
2. **Indicator score.** This is the mean of that indicator's answered items, rounded to the decimals in `REGLAS_PUNTUACION`, which is 2.
3. **Global score.** This is the weighted mean of the indicator scores. In the demo test all weights are 1.
4. **Rounding.** Halves always round up, so the result matches a manual check in Excel, as acceptance test PA-05 requires.
5. **Level.** The engine finds the `INTERPRETACIONES` range that contains the score. For example, 3.40 to 4.19 is Avanzado.
6. **Traceability.** Every result stores the test version, the scoring version and when it was computed.

A test without indicators and scoring rules cannot be scored. In the current Excel, DEMO-AGILE-50 is in that situation.
Such a test still appears in the operational figures, but it has no results.

### 2.4 Invitation states

The state is calculated live every time you look, using the rules in section 4.4:

| State | Rule |
|---|---|
| Realizado (completed) | The invitation has a completion date. |
| Pendiente (pending) | It has no completion date, and today is not past its expiry date. |
| Caducado (expired) | It has no completion date, and today is past its expiry date. |

Invitations expire after the test's expiry days, which default to 30.

---

## 3. Logging in and roles

The login screen lists one demo account per role. Click a role to enter.
This demo access has no passwords. In production, login would come from the platform, which is Base44 according to the document.
To switch roles, click "Salir" at the top right and choose another account.

Permissions are enforced on the server, not only by hiding buttons.
Even a hand-written request for data outside your role is refused.

| Role | What it can see in the Centro de mando |
|---|---|
| Administrador Agile Institute | All companies and tests, individual results, Excel downloads, the item-level answers export and the audit log. |
| Gestor de test | No access. The functional document gives this role users, sends, reports and states, but not dashboards. It sees a "Sin acceso" message. |
| Consultor | Only the companies assigned to it. In the demo that is Empresa Demo A. Asking for another company returns an access error. |
| Visor | Only dashboards expressly shared with it. In the demo that is Empresa Demo B with the demo test. It sees aggregates only: no names, no results table, and no individual sheet in the Excel. |

---

## 4. The screen, section by section

### 4.1 Top bar and side menu

The top bar shows the logged-in account, its role and the "Salir" button.

The side menu lists the six modules of the MVP.
Only "5 · Informes y cuadros de mando" is active, because this project implements that module.
The other five are shown greyed out for orientation.
On a phone, the menu collapses to the active module only.

### 4.2 Header

The header shows the page title and a scope line.
The scope line states which data you are allowed to see, reminds you that the data is fictitious, and shows when the figures were generated.
The "Descargar Excel" button opens the export dialog, described in section 5.

### 4.3 Filters ("Empresa", "Test", "Periodo de envío", "Desde", "Hasta")

Every number, chart and table on the page follows these filters, and so does the Excel download.

- **Empresa.** Choose one company or all the companies your role allows. The list only contains companies you are authorised to see.
- **Test.** Choose one test or "Todos los test". It defaults to the first test that has indicators, so the results charts show something straight away. Tests without scoring rules are marked "(sin indicadores)".
- **Periodo de envío.** The quick buttons "Todo", "30 días", "90 días" and "Este año" fill in the dates for you.
- **Desde / Hasta.** These set a custom date range. Typing a date clears the highlighted quick button.

The period always refers to the date the test was sent. One test sent in September and completed in October counts as a September send.
Any change reloads the page data immediately. There is no "apply" button.

### 4.4 KPI tiles

These tiles cover the first five indicators in section 7.

| Tile | How it is calculated |
|---|---|
| **Test enviados** (the large tile) | The number of invitations sent within the filters. The line underneath repeats which company and test are selected. |
| **Realizados** | Sent invitations that are completed. It has a green tick icon. |
| **Pendientes** | Sent invitations that are not completed and not yet expired. It has an amber icon. |
| **Caducados** | Sent invitations that expired without being completed. It has a red cross icon. |
| **Tasa de finalización** | Realizados divided by Test enviados. The bar is green at or above the pilot target of 80% and amber below it. The thin vertical mark shows the 80% target. |
| **Tiempo medio de respuesta** | The average time from sending to completion, in days, for completed tests only. The line underneath gives the median, which is less affected by a few very slow responses. |
| **Recordatorios enviados** | The number of reminder emails sent within the selected period, for the selected company and test. A reminder is sent once, three days after the send, if the test is still pending. |

Realizados, Pendientes and Caducados always add up to Test enviados.

### 4.5 Charts

Every chart has a "Ver tabla" link at its top right.
It swaps the chart for a plain table of the same numbers, which suits screen readers, copying values, or reading exact figures.
Click "Ver gráfico" to switch back.

Hovering over a bar, segment or point shows a tooltip with the exact values. The other marks fade so the hovered one stands out.

The charts also work in dark mode, which follows the operating system setting, and redraw to fit when the window is resized.

#### "Estado por empresa"

There is one horizontal bar per company, split into completed, pending and expired.
The colours are green, amber and red, and the legend repeats the status icons, so the chart is never read by colour alone.
The number at the end of each bar is the total sent to that company.
Use it to spot which company has many expired or pending tests.

#### "Actividad mensual"

This chart shows, month by month, how many tests were sent (blue) and how many were completed (orange).
Sends are counted by send month, and completions by completion month.
It shows the workload over time and whether completions keep up with sends.

#### "Resultado medio por indicador"

This chart only appears when a single test with indicators is selected.

- The first bar, in a darker colour, is the global result. The other bars are the test's indicators.
- Bars are drawn on the test's own scale, which is 1 to 5 for the demo test.
- The value and its level name are written at the end of each bar.
- The subtitle states how many results are included and which test and scoring versions they belong to.

Only results from one version of the test are averaged together. If results from older versions exist, they are left out, so different scoring rules are never mixed.

#### "Distribución por niveles"

This chart has one bar per indicator, plus the global result, and each bar always spans 100%.
Each bar is split by the percentage of results that fall into each level, from Inicial to Referente.
The colours go from light to dark blue as the level rises.
Percentages are written inside a segment only when they fit; otherwise use the tooltip or "Ver tabla".
Use it to see whether an average hides a split, such as a group with many people at both ends.

#### "Evolución temporal del resultado global"

This chart shows the average global result per completion month, as a line.

- Only comparable measurements are used, meaning the same test with the same test version and scoring version.
- A month with fewer results than the minimum sample, 3 by default, is not plotted. It still appears in the tooltip and table as "Muestra insuficiente". The line joins the valid months on either side of it.
- The chart only appears when at least two months have enough results. Otherwise it explains why it is empty. This follows section 7, which allows evolution only when there is more than one comparable measurement.
- The vertical axis zooms to the range of the data, so small changes are visible. Check the axis labels before reading a change as large.

#### Why a results chart can be empty

The three results charts show a message instead of a chart in these cases:

- "Selecciona un test…" means "Todos los test" is selected. Averages across different tests would be meaningless.
- The selected test has no indicators or scoring rules. This is the case for DEMO-AGILE-50.
- There are no completed results for the current filters.
- "Muestra insuficiente" means fewer results than the minimum sample, which is 3 by default. This protects people's privacy in small groups. Section 7 allows aggregated results only on an authorised sample.

### 4.6 "Resultados" table

Only the Administrador and Consultor roles see this table.

It lists every invitation within the filters, one row each.
The columns are person, company, position, test and version, state, sent date, completion date, days to respond, global score and level.

- **Search.** The search box matches person, company or position.
- **State filter.** The dropdown keeps only one state.
- **Sorting.** Click a column header to sort by it, and click it again to reverse the order. The default is the newest sends first.
- **Pages.** Results show 20 rows per page. Use "Anterior" and "Siguiente" to move between pages.

Search and the state filter only affect this table, not the charts above it.

### 4.7 Disclaimer

The note at the bottom states that scores are descriptive, not diagnostic.
It also states that results must not drive automated hiring, promotion or dismissal decisions, as section 8 and section 15 of the document require.

---

## 5. The Excel download

Click "Descargar Excel".
The dialog lists what the file will contain for your role, then "Descargar" downloads it.
The file always applies the filters currently on screen.

| Sheet | Contents | Who gets it |
|---|---|---|
| **Resumen** | The title, the active filters, the KPI table, the state by company, monthly activity, the averages by indicator, the level distribution and the monthly evolution. Each table has a native Excel chart beside it, in the same colours as the web page. | Everyone with access |
| **Resultados** | One row per invitation, including each indicator's score. It is an Excel table, so every column has a filter dropdown. The panes are frozen so names stay visible while scrolling. | Administrador and Consultor only |
| **Indicadores** | For each indicator: the mean, level, sample size, standard deviation, minimum, maximum and count per level. It also lists the level ranges. | Everyone with access, when results are available |
| **Trazabilidad** | Who downloaded the file and when, the role, the filters, the test and scoring versions, the minimum sample, and whether item-level answers are included. | Everyone with access |
| **Respuestas** | Every individual answer, item by item. | Administrador only, on request |

### Item-level answers export

By default the Excel never contains individual answers, as section 7 requires.
An administrator can include them by ticking "Incluir respuestas ítem a ítem (exportación administrativa)".
They must then write a reason of at least 10 characters, for example "verificación manual del cálculo PA-05".
The reason is written into the Trazabilidad sheet and into the audit log.

### Audit log

Every login and every Excel download is recorded with the person, time, filters, and whether item-level answers were included.
An administrator can read the latest 50 entries at http://127.0.0.1:8765/api/audit while logged in.

---

## 6. Settings

You can set these environment variables before starting the server, for example `$env:CDM_MIN_SAMPLE = "5"` in PowerShell.

| Variable | Default | Effect |
|---|---|---|
| `CDM_MIN_SAMPLE` | 3 | The minimum number of results before an average or level distribution is shown. |
| `CDM_DB_PATH` | `data/centro_test.db` | Where the database file lives. |
| `CDM_EXCEL_PATH` | The Excel master in `../Resources` | Which Excel master the importer reads. |
| `CDM_DEMO_LOGIN` | 1 | Set it to 0 to switch off the demo role picker. |

---

## 7. Where things live in the code

| File | Responsibility |
|---|---|
| `app/db.py` | The database tables, which follow the entities in section 5 of the document. |
| `app/seed.py` | The Excel import, its warnings, and the fictitious demo activity. |
| `app/scoring.py` | The scoring engine: reversing, means, rounding and levels. |
| `app/dashboard.py` | All the figures on the page, the state rules, the minimum-sample rule, and role permissions. |
| `app/export_xlsx.py` | Building the Excel file and its charts. |
| `app/main.py` | The web server: login, data endpoints, the download and the audit log. |
| `static/` | The web page: layout, styles, charts, results table and export dialog. |
| `tests/` | Automated checks for scoring, states, KPIs, permissions and the Excel contents. |

### Web API endpoints

All endpoints except login require a logged-in session. The data endpoints accept the filters `company_id`, `test_code`, `date_from` and `date_to`, with dates written as YYYY-MM-DD.

| Endpoint | Returns |
|---|---|
| `GET /api/auth/demo-accounts` | The demo accounts shown on the login screen. |
| `POST /api/auth/login` and `POST /api/auth/logout` | Start or end a session. |
| `GET /api/auth/me` | The current user, role and permissions. |
| `GET /api/filters` | The companies and tests your role may select. |
| `GET /api/dashboard` | The KPIs, chart data and results sections. |
| `GET /api/results` | The rows of the "Resultados" table. Administrador and Consultor only. |
| `GET /api/export.xlsx` | The Excel file. Add `include_responses=true&reason=…` for the item-level export. |
| `GET /api/audit` | The latest audit entries. Administrador only. |

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn` is not recognized | Run `python -m uvicorn app.main:app --port 8765` instead. |
| The page says the port is in use, or the server will not start | Another copy is already running. Stop it, or use a different port such as `--port 8766`. |
| The login screen shows no accounts | `CDM_DEMO_LOGIN` is set to 0. Remove it or set it to 1. |
| The results charts are empty | Select a single test with indicators, widen the period, or check that the sample reaches the minimum of 3. |
| A role sees less than expected | This is by design. Check the role table in section 3 of this guide. |
| The data looks stale or the dates look odd | Run `python -m app.seed`, then restart the server. |
