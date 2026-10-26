"""Construye la base de datos con el catálogo del libro de diseño y datos DEMO ficticios.

El libro de `Mejora/` se entrega vacío («No hay datos DEMO precargados»), así que aquí se generan capturas
ficticias con su mismo formato: dos organizaciones, ocho equipos, dos cortes (2026-04 y 2026-10), los cinco
cuestionarios y el pulso. Todas las filas llevan tipo_datos = DEMO e identificadores anónimos.
También se introducen tres errores de captura para que el control de calidad tenga algo que mostrar.

Uso:  python -m app.seed [--db RUTA]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sqlite3
from datetime import datetime

from . import db
from .catalog import Catalog, get_catalog
from .importer import insert_evaluation, insert_pulse
from .scoring import recompute_all

ORGS = [
    ("ORG-DC", "Demo Corp", [("EQ-DIR", "Dirección", 3), ("EQ-PRO", "Producto", 8), ("EQ-VEN", "Ventas", 9),
                             ("EQ-OPE", "Operaciones", 12), ("EQ-CLI", "Cliente", 10)]),
    ("ORG-DI", "Demo Industrial", [("EQ-PLA", "Planta", 9), ("EQ-ING", "Ingeniería", 7), ("EQ-LOG", "Logística", 4)]),
]
PERIODS = [("2026-04", 0.80, 0.0), ("2026-10", 0.90, 0.12)]   # periodo, participación, mejora media
TYPE = "DEMO"

STAFF = [
    ("admin@agileinstitute.es", "Administración Agile Institute", "admin", None, None),
    ("consultor@agileinstitute.es", "Consultor · Demo Corp", "consultor", None, "ORG-DC"),
    ("gestor@agileinstitute.es", "Gestor de test", "gestor", None, None),
    ("rrhh@democorp.demo", "RRHH · Demo Corp (solo lectura)", "rrhh", None, "ORG-DC"),
    ("lider@democorp.demo", "Líder de Producto · DC-PRO-01", "lider", "DC-PRO-01", "ORG-DC"),
    ("participante@democorp.demo", "Participante · DC-PRO-03", "participante", "DC-PRO-03", "ORG-DC"),
]


def _clip(x: float, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(round(x))))


def _people(conn: sqlite3.Connection) -> list[dict]:
    people = []
    for org_id, org_name, teams in ORGS:
        conn.execute("INSERT INTO organization(id, name) VALUES (?, ?)", (org_id, org_name))
        prefix = org_id.split("-")[1]
        for team_id, team_name, size in teams:
            conn.execute("INSERT INTO team(id, organization_id, name) VALUES (?,?,?)", (team_id, org_id, team_name))
            for n in range(1, size + 1):
                people.append({"id": f"{prefix}-{team_id.split('-')[1]}-{n:02d}", "org": org_id, "team": team_id,
                               "leader": n == 1 or team_id == "EQ-DIR" and n == 2})
    by_org: dict[str, list[dict]] = {}
    for p in people:
        by_org.setdefault(p["org"], []).append(p)
    for org_id, plist in by_org.items():
        top = plist[0]["id"]          # primer líder de la organización (Dirección / Planta)
        team_leader = {p["team"]: p["id"] for p in reversed(plist) if p["leader"] and p["id"].endswith("-01")}
        for p in plist:
            if p["id"] == top:
                p["resp"] = None
            elif p["leader"] and p["id"].endswith("-01"):
                p["resp"] = top
            else:
                p["resp"] = team_leader[p["team"]]
    conn.executemany("INSERT INTO person(id, organization_id, team_id, is_leader, responsable_id) VALUES (?,?,?,?,?)",
                     [(p["id"], p["org"], p["team"], int(p["leader"]), p["resp"]) for p in people])
    return people


def _answers(rng: random.Random, items, level: float, nv_rate: float = 0.025) -> dict[str, str]:
    out = {}
    for it, offset in items:
        r = rng.random()
        if r < nv_rate:
            out[it.item_id] = "NV"
        elif r < nv_rate + 0.01:
            continue      # omitida
        else:
            out[it.item_id] = str(_clip(level + offset + rng.gauss(0, 0.55), it.minimo, it.maximo))
    return out


def generate_demo(conn: sqlite3.Connection, catalog: Catalog, seed: int = 20261023) -> dict:
    rng = random.Random(seed)
    people = _people(conn)
    base = {p["id"]: rng.gauss(3.45, 0.42) for p in people}
    wellbeing = {p["id"]: rng.gauss(3.55, 0.5) for p in people}
    leader_style = {p["id"]: rng.gauss(3.7, 0.4) for p in people if p["leader"]}
    team_eff = {(t[0], code): rng.gauss(0, 0.15) for _, _, teams in ORGS for t in teams for code in catalog.tests}
    block_off = {(code, b["idx"]): rng.gauss(0, 0.28) for code, t in catalog.tests.items() for b in t.blocks}
    person_block = {(p["id"], code, b["idx"]): rng.gauss(0, 0.3)
                    for p in people for code, t in catalog.tests.items() for b in t.blocks}
    must_answer = {"DC-PRO-01", "DC-PRO-03"}
    n_eval = n_pulse = 0
    for periodo, participation, gain in PERIODS:
        day = 14 if periodo.endswith("04") else 20
        for p in people:
            if p["id"] not in must_answer and rng.random() > participation:
                continue
            fecha = f"{periodo}-{day + rng.randint(0, 8):02d}"
            for code, test in catalog.tests.items():
                if code == "T03" and not p["leader"]:
                    continue
                level = base[p["id"]] + gain + team_eff[(p["team"], code)]
                items = [(it, block_off[(code, it.block)] + person_block[(p["id"], code, it.block)])
                         for it in test.active_items]
                meta = {"evaluacion_id": f"{code}-{periodo}-{p['id']}", "persona_id": p["id"],
                        "organizacion_id": p["org"], "equipo_id": p["team"], "periodo": periodo,
                        "tipo_datos": TYPE, "fecha_iso": fecha}
                insert_evaluation(conn, code, test.version, meta, _answers(rng, items, level), "DEMO generado")
                n_eval += 1
            w = wellbeing[p["id"]] + gain
            pulse_items = []
            for item in catalog.pulse:
                if item.item_id == "ENPS":
                    continue
                if item.item_id.startswith("L"):
                    lvl = leader_style.get(p["resp"], 3.5) if p["resp"] else None
                else:
                    lvl = w
                pulse_items.append((item, lvl))
            answers = {}
            for item, lvl in pulse_items:
                if lvl is None:
                    answers[item.item_id] = "NV"
                elif rng.random() > 0.01:
                    answers[item.item_id] = str(_clip(lvl + rng.gauss(0, 0.6), item.minimo, item.maximo))
            answers["ENPS"] = str(_clip((w - 1) / 4 * 10 + rng.gauss(1.0, 1.6), 0, 10))
            meta = {"evaluacion_id": f"PUL-{periodo}-{p['id']}", "persona_id": p["id"], "organizacion_id": p["org"],
                    "equipo_id": p["team"], "periodo": periodo, "tipo_datos": TYPE, "fecha_iso": fecha,
                    "responsable_id": p["resp"]}
            insert_pulse(conn, meta, answers, "DEMO generado")
            n_pulse += 1
    _inject_quality_cases(conn, catalog)
    conn.commit()
    return {"people": len(people), "evaluations": n_eval, "pulses": n_pulse}


def _inject_quality_cases(conn: sqlite3.Connection, catalog: Catalog) -> None:
    """Tres capturas con errores (T01, 2026-10) para ver el control de calidad en el cuadro."""
    t01 = catalog.tests["T01"]
    ok = {i.item_id: "4" for i in t01.active_items}
    base = {"organizacion_id": "ORG-DC", "periodo": "2026-10", "tipo_datos": TYPE, "fecha_iso": "2026-10-22"}
    # METADATOS: falta equipo_id.
    insert_evaluation(conn, "T01", t01.version, base | {"evaluacion_id": "T01-2026-10-SIN-EQUIPO",
                                                        "persona_id": "DC-OPE-99", "equipo_id": ""}, ok, "DEMO error")
    # DUPLICADO: segunda captura de la misma persona y periodo (se marcan las dos).
    row = conn.execute("SELECT persona_id FROM evaluation WHERE test_code='T01' AND periodo='2026-10' "
                       "AND equipo_id='EQ-OPE' ORDER BY persona_id LIMIT 1").fetchone()
    insert_evaluation(conn, "T01", t01.version, base | {"evaluacion_id": "T01-2026-10-REPETIDA",
                                                        "persona_id": row["persona_id"], "equipo_id": "EQ-OPE"}, ok,
                      "DEMO error")
    # VALOR_INVALIDO: una respuesta fuera de la escala 1–5.
    target = conn.execute("SELECT id FROM evaluation WHERE test_code='T01' AND periodo='2026-10' "
                          "AND equipo_id='EQ-VEN' ORDER BY persona_id LIMIT 1").fetchone()
    conn.execute("UPDATE answer SET raw = '7' WHERE eval_id = ? AND item_id = ?", (target["id"], t01.active_items[0].item_id))


def _staff(conn: sqlite3.Connection) -> None:
    for email, name, role, persona, org in STAFF:
        cur = conn.execute("INSERT INTO staff_user(email, name, role, persona_id, organization_id) VALUES (?,?,?,?,?)",
                           (email, name, role, persona, org))
        if role == "consultor":
            conn.execute("INSERT INTO staff_org_access(staff_id, organization_id) VALUES (?,?)", (cur.lastrowid, org))


def _demo_plan(conn: sqlite3.Connection) -> None:
    actions = [
        {"plazo": "30 días", "accion": "Acordar criterios de priorización semanales", "responsable": "Líder",
         "fecha_limite": "2026-11-15", "estado": "En curso", "evidencia": ""},
        {"plazo": "60 días", "accion": "Definir qué tareas hace la persona y cuáles apoya la IA", "responsable": "Equipo",
         "fecha_limite": "2026-11-30", "estado": "Pendiente", "evidencia": ""},
        {"plazo": "90 días", "accion": "Revisar dependencias entre áreas cada mes", "responsable": "Coordinación",
         "fecha_limite": "2026-12-10", "estado": "Pendiente", "evidencia": ""},
    ]
    conn.execute("INSERT INTO action_plan(dashboard, scope_key, objetivo, actions, updated_by, updated_at) VALUES (?,?,?,?,?,?)",
                 ("equipo", "DEMO|2026-10|ORG-DC|EQ-PRO|TODOS", "Mejorar la coordinación y la priorización compartida",
                  json.dumps(actions, ensure_ascii=False), "seed", datetime.now().isoformat(timespec="seconds")))


def build_database(path: str, catalog: Catalog | None = None) -> tuple[sqlite3.Connection, dict]:
    catalog = catalog or get_catalog()
    if os.path.exists(path):
        os.remove(path)
    conn = db.connect(path)
    db.init_schema(conn)
    stats = generate_demo(conn, catalog)
    _staff(conn)
    _demo_plan(conn)
    conn.commit()
    stats["controls"] = {k: dict(v) for k, v in recompute_all(conn, catalog).items()}
    return conn, stats


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=os.environ.get("CDM_DB_PATH", db.DEFAULT_DB_PATH))
    args = ap.parse_args()
    conn, stats = build_database(args.db)
    print(f"Base creada en {os.path.abspath(args.db)}")
    print(f"Personas DEMO: {stats['people']} · evaluaciones: {stats['evaluations']} · pulsos: {stats['pulses']}")
    for code, c in stats["controls"].items():
        print(f"  {code}: {c}")
    conn.close()


if __name__ == "__main__":
    main()
