"""Exportación a Excel de un cuadro de mando (con los filtros activos).

Hojas:
- Cuadro: indicadores, competencias de cada cuestionario con gráfico de barras nativo, fortalezas y áreas.
- Pulso: indicadores de experiencia laboral por separado y eNPS independiente.
- Detalle: tablas propias del cuadro (equipos, cinco perfiles, puentes, conductas…), si las hay.
- Trazabilidad: autor, rol, filtros, versiones, mínimos y control de calidad.
- Datos_Txx: filas con el formato de captura, ítem a ítem. Solo administración y con motivo.
"""
from __future__ import annotations

import io
from datetime import datetime

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

NAVY = "0E3A4F"
TEAL = "1170A8"
PALE = "E6F1F5"
YELLOW = "F5C518"
HEAD = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor=NAVY)
TITLE = Font(bold=True, size=16, color=NAVY)
SUB = Font(italic=True, size=9, color="555555")
THIN = Border(bottom=Side(style="thin", color="D5DDE0"))

KPI_FMT = {"mean": "0.00", "enps": "+0;-0;0", "int": "0"}


def _header(ws, row, values, col=1):
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=col + i, value=v)
        c.font, c.fill = HEAD, HEAD_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)


def _table(ws, row, header, rows, col=1, number_format="0.00"):
    _header(ws, row, header, col)
    for r, values in enumerate(rows, start=1):
        for i, v in enumerate(values):
            c = ws.cell(row=row + r, column=col + i, value="—" if v is None else v)
            c.border = THIN
            if isinstance(v, float):
                c.number_format = number_format
    return row + len(rows) + 2


def _widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _sheet_cuadro(wb, data):
    ws = wb.active
    ws.title = "Cuadro"
    ws.sheet_view.showGridLines = False
    _widths(ws, [44, 14, 12, 12, 14, 4, 4, 4, 4])
    ws["A1"] = data["dashboard"]["title"]
    ws["A1"].font = TITLE
    ws["A2"] = data["dashboard"]["subtitle"]
    ws["A2"].font = SUB
    f = data["filters"]
    ws["A3"] = (f"Datos {f['tipo']} · periodo {f['periodo']} · organización {f['organizacion']} · equipo {f['equipo']}"
                f" · persona {f['persona']} · mínimo por grupo {data['min_group']}")
    ws["A3"].font = SUB
    row = 5
    _header(ws, row, ["Indicador", "Valor", "Detalle"])
    for k in data["kpis"]:
        row += 1
        ws.cell(row=row, column=1, value=k["label"]).border = THIN
        c = ws.cell(row=row, column=2, value="—" if k["value"] is None else k["value"])
        c.number_format = KPI_FMT.get(k["fmt"], "General")
        c.font = Font(bold=True, color=NAVY)
        c.border = THIN
        ws.cell(row=row, column=3, value=k["sub"]).font = SUB
    row += 3
    for code, p in data["profiles"].items():
        ws.cell(row=row, column=1, value=f"{code} · {p['name']} · v{p['version']} · {p['status']}").font = Font(bold=True, color=NAVY)
        row += 1
        start = row
        row = _table(ws, row, ["Competencia", "Media 1–5", "n válido", "Cobertura", "Desv. típica"],
                     [[b["name"], b["mean"], b["n"], b["coverage"], b["sd"]] for b in p["blocks"]])
        for r in range(start + 1, start + 9):
            ws.cell(row=r, column=4).number_format = "0%"
        chart = BarChart()
        chart.type = "bar"
        chart.style = 10
        chart.title = f"{code} · media por competencia"
        chart.y_axis.scaling.min = 1
        chart.y_axis.scaling.max = 5
        chart.y_axis.majorUnit = 1
        chart.x_axis.scaling.orientation = "maxMin"
        chart.legend = None
        chart.height, chart.width = 7.5, 15
        chart.add_data(Reference(ws, min_col=2, min_row=start, max_row=start + 8), titles_from_data=True)
        chart.set_categories(Reference(ws, min_col=1, min_row=start + 1, max_row=start + 8))
        chart.series[0].graphicalProperties.solidFill = TEAL if code != "T05" or len(data["profiles"]) == 1 else "C77A00"
        chart.series[0].graphicalProperties.line.noFill = True
        ws.add_chart(chart, f"G{start}")
        media = p["media"]
        ws.cell(row=row - 1, column=1, value=f"Media descriptiva (6 de 8): {media if media is not None else '—'} · "
                                            f"n con resumen {p['n_media']}").font = SUB
        row += 1
        for label, key in (("Fortalezas relativas", "strengths"), ("Áreas para explorar", "areas")):
            ws.cell(row=row, column=1, value=label + ": " + (", ".join(f"{x['name']} ({x['mean']})" for x in p[key]) or "—"))
            row += 1
        row += 9
    ws.cell(row=row, column=1, value=data["notice"]).font = SUB
    ws.cell(row=row + 1, column=1, value=data["disclaimer"]).font = SUB


def _sheet_pulso(wb, data):
    ws = wb.create_sheet("Pulso")
    _widths(ws, [10, 30, 62, 12, 10])
    p = data["pulse"]
    ws["A1"] = "Experiencia laboral · indicadores independientes"
    ws["A1"].font = TITLE
    ws["A2"] = p["source"] + ". Sin promedio global de Flow ni de bienestar; eNPS se calcula aparte."
    ws["A2"].font = SUB
    row = _table(ws, 4, ["Ítem", "Indicador", "Enunciado", "Media 1–5", "n"],
                 [[k, v["short"], v["text"], v["mean"], v["n"]] for k, v in p["items"].items()])
    e = p["enps"]
    _table(ws, row, ["eNPS", "n", "Promotores (9–10)", "Pasivos (7–8)", "Detractores (0–6)"],
           [[e["score"], e["n"], e["promoters"], e["passives"], e["detractors"]]], number_format="0.0")


def _sheet_detalle(wb, data):
    x = data["extras"]
    blocks = []
    if "teams" in x and x["teams"].get("rows"):
        hdr = ["Equipo", "n", "Media"] + (x["teams"].get("blocks") or [])
        blocks.append(("Resultados por equipo (solo equipos con muestra suficiente)", hdr,
                       [[t["team"], t["n"], t["media"]] + ((t["blocks"] or []) if x["teams"].get("blocks") else [])
                        for t in x["teams"]["rows"]]))
    if "five_profiles" in x:
        blocks.append(("Visión conjunta de los cinco perfiles · sin índice global", ["Test", "Ámbito", "Media", "n con resumen", "n con datos"],
                       [[p["test"], p["name"], p["media"], p["n_summary"], p["n_data"]] for p in x["five_profiles"]]))
    if "bridges" in x:
        blocks.append(("Puentes de lectura (propuesta, no validada)", ["Competencia A", "Media A", "Competencia B", "Media B", "Para conversar"],
                       [[b["a"]["name"], b["a"]["mean"], b["b"]["name"], b["b"]["mean"], b["prompt"]] for b in x["bridges"]]))
    if "behaviours" in x:
        rows = [["Más frecuente", b["item_id"], b["text"], b["mean"], b["n"]] for b in x["behaviours"]["top"]]
        rows += [["Menos frecuente", b["item_id"], b["text"], b["mean"], b["n"]] for b in x["behaviours"]["bottom"]]
        blocks.append(("Conductas a observar", ["Grupo", "Ítem", "Enunciado", "Media", "n"], rows))
    if "received" in x:
        blocks.append(("Percepción recibida del equipo (pulso L01–L03, mínimo 5)", ["Indicador", "Enunciado", "Media", "n"],
                       [[r["short"], r["text"], r["mean"], r["n"]] for r in x["received"]]))
    if "distribution" in x:
        blocks.append(("Cómo responde el grupo · personas por media redondeada", ["Competencia"] + x["distribution"]["labels"],
                       [[r["short"]] + (r["counts"] or ["oculto"] * 5) for r in x["distribution"]["rows"]]))
    if not blocks:
        return
    ws = wb.create_sheet("Detalle")
    _widths(ws, [34, 12, 40, 12, 50, 10, 10, 10, 10, 10, 10])
    row = 1
    for title, hdr, rows in blocks:
        ws.cell(row=row, column=1, value=title).font = Font(bold=True, color=NAVY, size=12)
        row = _table(ws, row + 1, hdr, rows)


def _sheet_traza(wb, data, actor, role, reason, with_data):
    ws = wb.create_sheet("Trazabilidad")
    _widths(ws, [32, 90])
    rows = [("Cuadro", data["dashboard"]["title"]), ("Generado", data["generated_at"]),
            ("Descargado por", f"{actor} · rol {role}"),
            ("Exportado", datetime.now().isoformat(timespec="seconds"))]
    rows += [(f"Filtro · {k}", v) for k, v in data["filters"].items() if k != "locked"]
    rows += [(f"Versión {t['code']}", f"{t['name']} · {t['version']} · escala {t['scale_id']}") for t in data["dashboard"]["tests"]]
    rows += [("Mínimo por grupo", data["min_group"]), ("Mínimo aplicado", data["min_n"]),
             ("Reglas", "Competencia con 2 de 3 ítems válidos; resumen con 6 de 8 competencias; NV y blanco no cuentan."),
             ("Datos ítem a ítem", "Sí · motivo: " + reason if with_data else "No incluidos")]
    rows += [(f"Control {k}", ", ".join(f"{s}: {n}" for s, n in v.items()) or "sin filas") for k, v in data["quality"].items()]
    rows += [("Aviso", data["notice"]), ("Uso", data["disclaimer"])]
    _table(ws, 1, ["Campo", "Valor"], rows)


def _sheet_datos(wb, tables):
    for code, t in tables.items():
        ws = wb.create_sheet(f"Datos_{code}")
        ws.append(t["header"])
        for r in t["rows"]:
            ws.append(r)
        if t["rows"]:
            ref = f"A1:{get_column_letter(len(t['header']))}{len(t['rows']) + 1}"
            tab = Table(displayName=f"tbl{code}", ref=ref)
            tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
            ws.add_table(tab)
        ws.freeze_panes = "C2"


def build_workbook(data: dict, actor: str, role: str, data_tables: dict | None = None, reason: str | None = None) -> bytes:
    wb = Workbook()
    _sheet_cuadro(wb, data)
    _sheet_pulso(wb, data)
    _sheet_detalle(wb, data)
    _sheet_traza(wb, data, actor, role, reason, data_tables is not None)
    if data_tables:
        _sheet_datos(wb, data_tables)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
