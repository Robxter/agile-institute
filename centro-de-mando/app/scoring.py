"""Motor de cálculo descriptivo: reproduce las columnas azules de Datos_T01…T05 y Datos_PULSO.

- control: METADATOS si falta un dato obligatorio o el tipo no es REAL/DEMO; DUPLICADO si se repite
  evaluacion_id, o persona + periodo + tipo, dentro del mismo cuestionario; VALOR_INVALIDO si una respuesta
  no es entera dentro del rango; si no, OK. Solo las filas OK entran en los cuadros.
- Competencia (bloque): media de sus ítems válidos si hay al menos 2 de 3. NV y blanco no cuentan.
- media_descriptiva: media de las competencias calculadas si hay al menos 6 de 8.
No hay baremos ni niveles A1–A5: los resultados son medias descriptivas 1–5.
"""
from __future__ import annotations

import sqlite3
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal

from .catalog import Catalog, Test

MIN_ITEMS_PER_BLOCK = 2
MIN_BLOCKS_FOR_SUMMARY = 6
CONTROL_OK = "OK"


def round_half_up(x: float | None, decimals: int = 2) -> float | None:
    if x is None:
        return None
    q = Decimal(1).scaleb(-decimals)
    return float(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))


def parse_raw(raw: str | None, lo: int, hi: int) -> tuple[str, int | None]:
    """('num', v) · ('nv', None) · ('blank', None) · ('bad', None)."""
    if raw is None or str(raw).strip() == "":
        return "blank", None
    s = str(raw).strip()
    if s.upper() == "NV":
        return "nv", None
    try:
        f = float(s.replace(",", "."))
    except ValueError:
        return "bad", None
    if f != int(f) or not lo <= f <= hi:
        return "bad", None
    return "num", int(f)


def metadata_ok(row) -> bool:
    required = ("evaluacion_id", "persona_id", "organizacion_id", "equipo_id", "periodo", "fecha_iso")
    if any(not (row[k] or "").strip() for k in required):
        return False
    return row["tipo_datos"] in ("REAL", "DEMO")


def block_scores(test: Test, values: dict[str, int | None]) -> tuple[list[tuple[int, float | None, int]], float | None]:
    """values: item_id -> número válido (ya invertido si procede) o None."""
    item_by_id = {i.item_id: i for i in test.items}
    out = []
    for b in test.blocks:
        nums = []
        for iid in b["items"]:
            v = values.get(iid)
            if v is not None:
                it = item_by_id[iid]
                nums.append(it.minimo + it.maximo - v if it.inverse else v)
        score = sum(nums) / len(nums) if len(nums) >= MIN_ITEMS_PER_BLOCK else None
        out.append((b["idx"], score, len(nums)))
    valid = [s for _, s, _ in out if s is not None]
    media = sum(valid) / len(valid) if len(valid) >= MIN_BLOCKS_FOR_SUMMARY else None
    return out, media


def recompute_test(conn: sqlite3.Connection, test: Test) -> Counter:
    """Recalcula control, competencias y media de todas las filas de un cuestionario."""
    rows = conn.execute("SELECT * FROM evaluation WHERE test_code = ?", (test.code,)).fetchall()
    id_count = Counter(r["evaluacion_id"] for r in rows)
    cut_count = Counter((r["persona_id"], r["periodo"], r["tipo_datos"]) for r in rows)
    answers: dict[int, dict[str, str]] = {}
    for a in conn.execute("SELECT a.eval_id, a.item_id, a.raw FROM answer a JOIN evaluation e ON e.id = a.eval_id "
                          "WHERE e.test_code = ?", (test.code,)):
        answers.setdefault(a["eval_id"], {})[a["item_id"]] = a["raw"]
    item_by_id = {i.item_id: i for i in test.active_items}
    tally = Counter()
    conn.execute("DELETE FROM block_score WHERE eval_id IN (SELECT id FROM evaluation WHERE test_code = ?)", (test.code,))
    for r in rows:
        raw = answers.get(r["id"], {})
        parsed = {iid: parse_raw(raw.get(iid), it.minimo, it.maximo) for iid, it in item_by_id.items()}
        if not metadata_ok(r):
            control = "METADATOS"
        elif id_count[r["evaluacion_id"]] > 1 or cut_count[(r["persona_id"], r["periodo"], r["tipo_datos"])] > 1:
            control = "DUPLICADO"
        elif any(k == "bad" for k, _ in parsed.values()):
            control = "VALOR_INVALIDO"
        else:
            control = CONTROL_OK
        tally[control] += 1
        media, n_blocks = None, 0
        if control == CONTROL_OK:
            blocks, media = block_scores(test, {iid: v for iid, (k, v) in parsed.items() if k == "num"})
            n_blocks = sum(1 for _, s, _ in blocks if s is not None)
            conn.executemany("INSERT INTO block_score(eval_id, block, score, n_valid) VALUES (?,?,?,?)",
                             [(r["id"], idx, s, n) for idx, s, n in blocks])
        conn.execute("UPDATE evaluation SET control = ?, media_descriptiva = ?, n_blocks = ? WHERE id = ?",
                     (control, media, n_blocks, r["id"]))
    conn.commit()
    return tally


def recompute_pulse(conn: sqlite3.Connection, catalog: Catalog) -> Counter:
    rows = conn.execute("SELECT * FROM pulse").fetchall()
    id_count = Counter(r["evaluacion_id"] for r in rows)
    cut_count = Counter((r["persona_id"], r["periodo"], r["tipo_datos"]) for r in rows)
    answers: dict[int, dict[str, str]] = {}
    for a in conn.execute("SELECT pulse_id, item_id, raw FROM pulse_answer"):
        answers.setdefault(a["pulse_id"], {})[a["item_id"]] = a["raw"]
    tally = Counter()
    for r in rows:
        raw = answers.get(r["id"], {})
        bad = any(parse_raw(raw.get(p.item_id), p.minimo, p.maximo)[0] == "bad" for p in catalog.pulse)
        if not metadata_ok(r):
            control = "METADATOS"
        elif id_count[r["evaluacion_id"]] > 1 or cut_count[(r["persona_id"], r["periodo"], r["tipo_datos"])] > 1:
            control = "DUPLICADO"
        elif bad:
            control = "VALOR_INVALIDO"
        else:
            control = CONTROL_OK
        tally[control] += 1
        conn.execute("UPDATE pulse SET control = ? WHERE id = ?", (control, r["id"]))
    conn.commit()
    return tally


def recompute_all(conn: sqlite3.Connection, catalog: Catalog) -> dict[str, Counter]:
    out = {code: recompute_test(conn, t) for code, t in catalog.tests.items()}
    out["PULSO"] = recompute_pulse(conn, catalog)
    return out
