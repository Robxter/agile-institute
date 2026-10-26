"""Importación de capturas con el formato del libro de diseño (hojas Datos_T01…Datos_T05 y Datos_PULSO).

Encabezados estables: evaluacion_id, persona_id, organizacion_id, equipo_id, periodo, tipo_datos, fecha_iso,
los ítems del cuestionario y, en el pulso, responsable_id. Las columnas calculadas (control, bloque_n,
media_descriptiva, incluido_*) se ignoran: se recalculan aquí con las mismas reglas.

Una fila con un evaluacion_id ya existente en ese cuestionario sustituye a la anterior.
Las organizaciones, equipos y personas que no existan se crean con su identificador anónimo.

Uso:  python -m app.importer RUTA.xlsx [--db RUTA]
"""
from __future__ import annotations

import argparse
import sqlite3
from datetime import date, datetime

import openpyxl

from . import db
from .catalog import Catalog, get_catalog
from .scoring import recompute_all

META = ("evaluacion_id", "persona_id", "organizacion_id", "equipo_id", "periodo", "tipo_datos", "fecha_iso")


def _cell(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _periodo(v) -> str:
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m")
    return _cell(v)


def ensure_people(conn: sqlite3.Connection, persona: str, org: str, team: str, responsable: str | None = None) -> None:
    if org:
        conn.execute("INSERT OR IGNORE INTO organization(id, name) VALUES (?, ?)", (org, org))
    if org and team:
        conn.execute("INSERT OR IGNORE INTO team(id, organization_id, name) VALUES (?, ?, ?)", (team, org, team))
    if persona and org and team:
        conn.execute("INSERT OR IGNORE INTO person(id, organization_id, team_id) VALUES (?, ?, ?)", (persona, org, team))
        if responsable:
            conn.execute("UPDATE person SET responsable_id = ? WHERE id = ?", (responsable, persona))
    if responsable and org and team:
        conn.execute("INSERT OR IGNORE INTO person(id, organization_id, team_id, is_leader) VALUES (?, ?, ?, 1)",
                     (responsable, org, team))
        conn.execute("UPDATE person SET is_leader = 1 WHERE id = ?", (responsable,))


def insert_evaluation(conn: sqlite3.Connection, test_code: str, version: str, meta: dict, answers: dict[str, str],
                      source: str, replace: bool = True) -> None:
    if replace and meta.get("evaluacion_id"):
        conn.execute("DELETE FROM evaluation WHERE test_code = ? AND evaluacion_id = ?", (test_code, meta["evaluacion_id"]))
    cur = conn.execute(
        """INSERT INTO evaluation(evaluacion_id, test_code, persona_id, organizacion_id, equipo_id, periodo, tipo_datos,
                                  fecha_iso, test_version, source) VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (meta.get("evaluacion_id"), test_code, meta.get("persona_id"), meta.get("organizacion_id"), meta.get("equipo_id"),
         meta.get("periodo"), meta.get("tipo_datos"), meta.get("fecha_iso"), version, source))
    conn.executemany("INSERT INTO answer(eval_id, item_id, raw) VALUES (?,?,?)",
                     [(cur.lastrowid, k, v) for k, v in answers.items() if v != ""])


def insert_pulse(conn: sqlite3.Connection, meta: dict, answers: dict[str, str], source: str, replace: bool = True) -> None:
    if replace and meta.get("evaluacion_id"):
        conn.execute("DELETE FROM pulse WHERE evaluacion_id = ?", (meta["evaluacion_id"],))
    cur = conn.execute(
        """INSERT INTO pulse(evaluacion_id, persona_id, organizacion_id, equipo_id, periodo, tipo_datos, fecha_iso,
                             responsable_id, source) VALUES (?,?,?,?,?,?,?,?,?)""",
        (meta.get("evaluacion_id"), meta.get("persona_id"), meta.get("organizacion_id"), meta.get("equipo_id"),
         meta.get("periodo"), meta.get("tipo_datos"), meta.get("fecha_iso"), meta.get("responsable_id") or None, source))
    conn.executemany("INSERT INTO pulse_answer(pulse_id, item_id, raw) VALUES (?,?,?)",
                     [(cur.lastrowid, k, v) for k, v in answers.items() if v != ""])


def import_workbook(conn: sqlite3.Connection, path: str, catalog: Catalog | None = None, source: str | None = None) -> dict:
    catalog = catalog or get_catalog()
    source = source or path
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    report: dict[str, int] = {}
    sheets = [(f"Datos_{c}", c) for c in catalog.tests] + [("Datos_PULSO", "PULSO")]
    for sheet, code in sheets:
        if sheet not in wb.sheetnames:
            continue
        it = wb[sheet].iter_rows(values_only=True)
        header = [_cell(h) for h in next(it, [])]
        if code == "PULSO":
            item_ids = [p.item_id for p in catalog.pulse]
        else:
            item_ids = [i.item_id for i in catalog.tests[code].active_items]
        missing = [h for h in META + tuple(item_ids) if h not in header]
        if missing:
            raise ValueError(f"{sheet}: faltan columnas {', '.join(missing)}.")
        pos = {h: header.index(h) for h in header if h}
        parsed = []
        for row in it:
            values = {h: (_periodo(row[i]) if h == "periodo" else _cell(row[i])) for h, i in pos.items() if i < len(row)}
            if not any(values.get(h) for h in META + tuple(item_ids)):
                continue   # fila vacía de la plantilla
            meta = {h: values.get(h, "") for h in META}
            meta["tipo_datos"] = meta["tipo_datos"].upper()
            if code == "PULSO":
                meta["responsable_id"] = values.get("responsable_id", "")
            parsed.append((meta, {iid: values.get(iid, "") for iid in item_ids}))
        # Primero se retiran las versiones anteriores de esos evaluacion_id; después se insertan todas las filas,
        # así un id repetido dentro del mismo fichero queda marcado como DUPLICADO en lugar de sustituirse.
        ids = sorted({m["evaluacion_id"] for m, _ in parsed if m["evaluacion_id"]})
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            q = ",".join("?" * len(chunk))
            if code == "PULSO":
                conn.execute(f"DELETE FROM pulse WHERE evaluacion_id IN ({q})", chunk)
            else:
                conn.execute(f"DELETE FROM evaluation WHERE test_code = ? AND evaluacion_id IN ({q})", [code] + chunk)
        for meta, answers in parsed:
            if code == "PULSO":
                ensure_people(conn, meta["persona_id"], meta["organizacion_id"], meta["equipo_id"], meta["responsable_id"])
                insert_pulse(conn, meta, answers, source, replace=False)
            else:
                ensure_people(conn, meta["persona_id"], meta["organizacion_id"], meta["equipo_id"])
                insert_evaluation(conn, code, catalog.tests[code].version, meta, answers, source, replace=False)
        report[code] = len(parsed)
    wb.close()
    conn.commit()
    controls = recompute_all(conn, catalog)
    return {"rows": report, "controls": {k: dict(v) for k, v in controls.items()}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("xlsx")
    ap.add_argument("--db", default=None)
    args = ap.parse_args()
    conn = db.connect(args.db)
    db.init_schema(conn)
    rep = import_workbook(conn, args.xlsx)
    for code, n in rep["rows"].items():
        print(f"{code}: {n} filas · control {rep['controls'].get(code, {})}")


if __name__ == "__main__":
    main()
