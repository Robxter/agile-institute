"""Visual Excel export of the Centro de mando (section 7, PA-09).

Contents: visual summary with native charts, filterable result table, authorised aggregated indicators and
traceability. Item-level answers only when an administrator expressly authorises it (with a reason).
Styling follows the DASHBOARD_DEMO sheet of the Excel maestro (header fill 0B3A4A, white bold text).
"""
from __future__ import annotations

import io
from datetime import datetime

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

BRAND = "0B3A4A"
MUTED = "52666D"
HEADER_FILL = PatternFill("solid", fgColor=BRAND)
HEADER_FONT = Font(bold=True, color="FFFFFF")
TITLE_FONT = Font(bold=True, size=16, color=BRAND)
SECTION_FONT = Font(bold=True, size=12, color=BRAND)
NOTE_FONT = Font(italic=True, size=9, color=MUTED)
THIN = Side(style="thin", color="E1E0D9")
CELL_BORDER = Border(bottom=THIN)

# Reference data-viz palette: status colours (fixed) and an ordinal blue ramp for levels.
STATUS_COLORS = {"completed": "0CA30C", "pending": "FAB219", "expired": "D03B3B"}
SERIES_BLUE = "2A78D6"
SERIES_ORANGE = "EB6834"
ORDINAL_RAMP = ["86B6EF", "5598E7", "2A78D6", "1C5CAB", "104281", "0D366B"]


def _ordinal(n: int) -> list[str]:
    if n <= 1:
        return [ORDINAL_RAMP[2]]
    step = (len(ORDINAL_RAMP) - 1) / (n - 1)
    return [ORDINAL_RAMP[round(k * step)] for k in range(n)]


def _header(ws, row: int, values: list[str], col: int = 1) -> None:
    for k, v in enumerate(values):
        c = ws.cell(row=row, column=col + k, value=v)
        c.fill, c.font = HEADER_FILL, HEADER_FONT
        c.alignment = Alignment(vertical="center", wrap_text=True)


def _row(ws, row: int, values: list, col: int = 1, fmt: dict | None = None) -> None:
    for k, v in enumerate(values):
        c = ws.cell(row=row, column=col + k, value=v)
        c.border = CELL_BORDER
        if fmt and k in fmt:
            c.number_format = fmt[k]


def _dt(iso: str | None):
    return datetime.fromisoformat(iso) if iso else None


def _axes(chart) -> None:
    """openpyxl >= 3.1 hides axes unless told otherwise; show both with a recessive grid."""
    from openpyxl.chart.shapes import GraphicalProperties
    chart.x_axis.delete = False
    chart.y_axis.delete = False
    grid = GraphicalProperties()
    grid.line.solidFill = "E1E0D9"
    if chart.y_axis.majorGridlines is not None:
        chart.y_axis.majorGridlines.spPr = grid
    # Keep title and legend outside the plot area so they never cover axis labels.
    if chart.title is not None:
        chart.title.overlay = False
    if chart.legend is not None:
        chart.legend.overlay = False
    # Horizontal bars listed top-down (maxMin) keep their value axis at the bottom.
    if getattr(chart, "type", None) == "bar" and chart.x_axis.scaling.orientation == "maxMin":
        chart.y_axis.crosses = "max"


def _color_series(chart, colors: list[str]) -> None:
    for s, color in zip(chart.series, colors):
        s.graphicalProperties.solidFill = color
        s.graphicalProperties.line.solidFill = color


def build_workbook(data: dict, table: dict | None, items: list[dict] | None, actor: str, reason: str | None) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen"
    ws.sheet_view.showGridLines = False
    k = data["kpis"]
    res = data["results"]

    ws["A1"] = "Centro de mando · Centro de Test"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = "Agile Institute · Informes y cuadros de mando"
    ws["A2"].font = Font(color=MUTED)
    ws["A3"] = f"Generado el {data['generated_at'].replace('T', ' ')} por {actor}. Datos autorizados según rol ({data['scope']['role']})."
    ws["A3"].font = NOTE_FONT

    r = 5
    for label, value in data["filters"].items():
        ws.cell(row=r, column=1, value=label).font = Font(bold=True, color=BRAND)
        ws.cell(row=r, column=2, value=value)
        r += 1

    # KPI block (mirrors DASHBOARD_DEMO: Indicador | Valor)
    r += 1
    ws.cell(row=r, column=1, value="Indicadores operativos").font = SECTION_FONT
    r += 1
    _header(ws, r, ["Indicador", "Valor"])
    kpi_rows = [
        ("Test enviados", k["sent"], "0"),
        ("Realizados", k["completed"], "0"),
        ("Pendientes", k["pending"], "0"),
        ("Caducados", k["expired"], "0"),
        ("Tasa de finalización", k["completion_rate"], "0.0%"),
        ("Tiempo medio de respuesta (días)", k["avg_response_days"], "0.0"),
        ("Tiempo mediano de respuesta (días)", k["median_response_days"], "0.0"),
        ("Recordatorios enviados", k["reminders"], "0"),
    ]
    for label, value, fmt in kpi_rows:
        r += 1
        _row(ws, r, [label, value if value is not None else "—"], fmt={1: fmt})

    # Status by company + stacked bar chart
    r += 2
    ws.cell(row=r, column=1, value="Estado de los envíos por empresa").font = SECTION_FONT
    r += 1
    status_top = r
    _header(ws, r, ["Empresa", "Realizados", "Pendientes", "Caducados", "Enviados"])
    for row in data["status_by_company"]:
        r += 1
        _row(ws, r, [row["company"], row["completed"], row["pending"], row["expired"], row["sent"]])
    if data["status_by_company"]:
        ch = BarChart()
        ch.type, ch.grouping, ch.overlap = "bar", "stacked", 100
        ch.title = "Estado por empresa"
        ch.add_data(Reference(ws, min_col=2, max_col=4, min_row=status_top, max_row=r), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=status_top + 1, max_row=r))
        _color_series(ch, [STATUS_COLORS["completed"], STATUS_COLORS["pending"], STATUS_COLORS["expired"]])
        ch.x_axis.scaling.orientation = "maxMin"
        ch.gapWidth, ch.height, ch.width = 60, 7, 16
        ch.y_axis.majorGridlines = None
        ch.legend.position = "b"
        _axes(ch)
        ws.add_chart(ch, "J5")

    # Activity per month
    r += 2
    ws.cell(row=r, column=1, value="Actividad mensual").font = SECTION_FONT
    r += 1
    act_top = r
    _header(ws, r, ["Mes", "Enviados", "Realizados"])
    for a in data["activity"]:
        r += 1
        _row(ws, r, [a["period"], a["sent"], a["completed"]])
    if len(data["activity"]) > 1:
        ch = BarChart()
        ch.type = "col"
        ch.title = "Envíos y realizados por mes"
        ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=act_top, max_row=r), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=act_top + 1, max_row=r))
        _color_series(ch, [SERIES_BLUE, SERIES_ORANGE])
        ch.gapWidth, ch.height, ch.width = 80, 7, 16
        ch.legend.position = "b"
        _axes(ch)
        ws.add_chart(ch, "J21")

    # Results section
    r += 2
    ws.cell(row=r, column=1, value="Resultados por indicador").font = SECTION_FONT
    r += 1
    if not res.get("available") or res.get("suppressed"):
        ws.cell(row=r, column=1, value=res.get("reason")).font = NOTE_FONT
    else:
        ws.cell(row=r, column=1, value=(f"n = {res['n']} resultados · test v{res['test_version']} · "
                                        f"puntuación v{res['scoring_version']} · escala {res['scale']['min']:g}-{res['scale']['max']:g}")).font = NOTE_FONT
        r += 1
        means_top = r
        _header(ws, r, ["Indicador medido", "Media", "Nivel", "n", "Mín.", "Máx."])
        for m in res["means"]:
            r += 1
            _row(ws, r, [m["name"], m["mean"], m["level"], m["n"], m["min"], m["max"]], fmt={1: "0.00"})
        ch = BarChart()
        ch.type = "bar"
        ch.title = f"Resultado medio por indicador ({res['scale']['min']:g}-{res['scale']['max']:g})"
        ch.add_data(Reference(ws, min_col=2, min_row=means_top, max_row=r), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=means_top + 1, max_row=r))
        _color_series(ch, [SERIES_BLUE])
        ch.x_axis.scaling.orientation = "maxMin"
        ch.y_axis.scaling.min, ch.y_axis.scaling.max = res["scale"]["min"], res["scale"]["max"]
        ch.legend = None
        ch.dataLabels = DataLabelList()
        ch.dataLabels.showVal = True
        ch.dataLabels.showSerName = False
        ch.dataLabels.showCatName = False
        ch.dataLabels.showLegendKey = False
        ch.dataLabels.numFmt = "0.00"
        ch.gapWidth, ch.height, ch.width = 70, 7, 16
        _axes(ch)
        ws.add_chart(ch, "J37")

        r += 2
        ws.cell(row=r, column=1, value="Distribución por niveles").font = SECTION_FONT
        r += 1
        dist_top = r
        level_names = [l["name"] for l in res["levels"]]
        _header(ws, r, ["Indicador"] + level_names + ["Total"])
        for d in res["distribution"]:
            r += 1
            _row(ws, r, [d["name"]] + [c["count"] for c in d["counts"]] + [d["total"]])
        ch = BarChart()
        ch.type, ch.grouping, ch.overlap = "bar", "percentStacked", 100
        ch.title = "Distribución por niveles (% de resultados)"
        ch.add_data(Reference(ws, min_col=2, max_col=1 + len(level_names), min_row=dist_top, max_row=r), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=dist_top + 1, max_row=r))
        _color_series(ch, _ordinal(len(level_names)))
        ch.x_axis.scaling.orientation = "maxMin"
        ch.gapWidth, ch.height, ch.width = 60, 7, 16
        ch.legend.position = "b"
        _axes(ch)
        ws.add_chart(ch, "J53")

        r += 2
        ws.cell(row=r, column=1, value="Evolución temporal del resultado global").font = SECTION_FONT
        r += 1
        evo = res["evolution"]
        if not evo["available"]:
            ws.cell(row=r, column=1, value=evo["reason"]).font = NOTE_FONT
        else:
            evo_top = r
            _header(ws, r, ["Mes", "Media global", "n"])
            for p in evo["series"]:
                r += 1
                _row(ws, r, [p["period"], p["mean"] if not p["suppressed"] else None, p["n"]], fmt={1: "0.00"})
            ch = LineChart()
            ch.title = "Evolución mensual del resultado global"
            ch.add_data(Reference(ws, min_col=2, min_row=evo_top, max_row=r), titles_from_data=True)
            ch.set_categories(Reference(ws, min_col=1, min_row=evo_top + 1, max_row=r))
            s = ch.series[0]
            s.graphicalProperties.line.solidFill = SERIES_BLUE
            s.graphicalProperties.line.width = 25400  # 2pt
            s.marker.symbol = "circle"
            s.marker.size = 7
            s.marker.graphicalProperties.solidFill = SERIES_BLUE
            s.marker.graphicalProperties.line.solidFill = SERIES_BLUE
            s.smooth = False
            ch.y_axis.scaling.min, ch.y_axis.scaling.max = res["scale"]["min"], res["scale"]["max"]
            ch.legend = None
            ch.height, ch.width = 7, 16
            _axes(ch)
            ws.add_chart(ch, "J69")

    ws.column_dimensions["A"].width = 36
    for col in "BCDEF":
        ws.column_dimensions[col].width = 15

    # Resultados: filterable table (only for roles allowed to see individuals)
    if table is not None:
        wt = wb.create_sheet("Resultados")
        ind = table["indicators"]
        headers = (["Invitación", "Empresa", "Persona", "Posición", "Test", "Versión", "Estado", "Enviado", "Caduca",
                    "Realizado", "Días de respuesta", "Recordatorio", "Resultado global", "Nivel"]
                   + [i["name"] for i in ind])
        _header(wt, 1, headers)
        for n, row in enumerate(table["rows"], start=2):
            values = [row["invitation_code"], row["company"], row["person"], row["position"], row["test_name"],
                      row["test_version"], row["status_label"], _dt(row["sent_at"]), _dt(row["expires_at"]),
                      _dt(row["completed_at"]), row["response_days"], _dt(row["reminder_sent_at"]), row["global"],
                      row["level"]] + [row["scores"].get(i["code"]) for i in ind]
            for c, v in enumerate(values, start=1):
                cell = wt.cell(row=n, column=c, value=v)
                if c in (8, 9, 10, 12):
                    cell.number_format = "dd/mm/yyyy hh:mm"
                elif c == 11:
                    cell.number_format = "0.0"
                elif c == 13 or c > 14:
                    cell.number_format = "0.00"
        last = max(2, len(table["rows"]) + 1)
        if not table["rows"]:
            wt.cell(row=2, column=1, value="Sin resultados para los filtros elegidos")
        tab = Table(displayName="Resultados", ref=f"A1:{get_column_letter(len(headers))}{last}")
        tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        wt.add_table(tab)
        wt.freeze_panes = "D2"
        widths = [12, 18, 22, 20, 26, 9, 12, 17, 17, 17, 10, 17, 11, 14] + [14] * len(ind)
        for c, w in enumerate(widths, start=1):
            wt.column_dimensions[get_column_letter(c)].width = w

    # Indicadores agregados autorizados
    wi = wb.create_sheet("Indicadores")
    if res.get("available") and not res.get("suppressed"):
        level_names = [l["name"] for l in res["levels"]]
        _header(wi, 1, ["Código", "Indicador", "Media", "Nivel", "n", "Desv. típica", "Mín.", "Máx."] + level_names)
        dist = {d["code"]: d for d in res["distribution"]}
        for n, m in enumerate(res["means"], start=2):
            counts = [c["count"] for c in dist[m["code"]]["counts"]]
            _row(wi, n, [m["code"], m["name"], m["mean"], m["level"], m["n"], m["sd"], m["min"], m["max"]] + counts,
                 fmt={2: "0.00", 5: "0.00"})
        r = len(res["means"]) + 3
        _header(wi, r, ["Nivel", "Desde", "Hasta"])
        for l in res["levels"]:
            r += 1
            _row(wi, r, [l["name"], l["min"], l["max"]])
        wi.column_dimensions["B"].width = 26
    else:
        wi["A1"] = res.get("reason")
        wi["A1"].font = NOTE_FONT

    # Trazabilidad
    wtz = wb.create_sheet("Trazabilidad")
    _header(wtz, 1, ["Campo", "Valor"])
    info = [("Generado", data["generated_at"]), ("Generado por", actor), ("Rol", data["scope"]["role"])]
    info += [(f"Filtro · {k2}", v) for k2, v in data["filters"].items()]
    if res.get("available"):
        info += [("Versión de test", res["test_version"]), ("Versión de puntuación", res["scoring_version"]),
                 ("Muestra mínima para agregados", res["min_sample"]),
                 ("Resultados de otras versiones excluidos", res["excluded_other_versions"])]
    info += [("Respuestas ítem a ítem", "Incluidas (exportación administrativa autorizada)" if items is not None else "No incluidas"),
             ("Motivo de la exportación administrativa", reason or "—"),
             ("Advertencia", "Puntuaciones descriptivas, no diagnósticas. No usar para decisiones automatizadas de empleo.")]
    for n, (a, b) in enumerate(info, start=2):
        _row(wtz, n, [a, b])
    wtz.column_dimensions["A"].width = 40
    wtz.column_dimensions["B"].width = 80

    if items is not None:
        wr = wb.create_sheet("Respuestas")
        headers = ["Invitación", "Empresa", "Persona", "Test", "Versión", "Ítem", "Indicador", "Texto", "Invertido", "Valor", "Fecha"]
        _header(wr, 1, headers)
        for n, it in enumerate(items, start=2):
            _row(wr, n, [it["invitation_code"], it["company"], it["person"], it["test_code"], it["test_version"],
                         it["item_code"], it["indicator_code"], it["item_text"], "Sí" if it["reverse_scored"] else "No",
                         it["value"], _dt(it["answered_at"])])
        if items:
            tab = Table(displayName="Respuestas", ref=f"A1:K{len(items) + 1}")
            tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
            wr.add_table(tab)
        wr.column_dimensions["H"].width = 60

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
