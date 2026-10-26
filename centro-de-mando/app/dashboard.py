"""Cuadros de mando por dimensión profesional.

Siete cuadros, cada uno con su cuestionario (o pareja de cuestionarios) y el pulso de experiencia laboral:

| Cuadro        | Fuente      | Lectura                                                            |
|---------------|-------------|--------------------------------------------------------------------|
| persona       | T01         | Agilidad personal, individual o de grupo                           |
| equipo        | T02         | Contribución individual al equipo, agregada (mínimo 5)             |
| liderazgo     | T03 + pulso | Autopercepción del líder y percepción recibida de su equipo (L01–L03) |
| organizacion  | T04 + T01–T05 | Ocho competencias T04 y visión conjunta de los cinco perfiles    |
| ia            | T05         | IA transversal: competencias, equipos y conductas                  |
| persona_ia    | T01 + T05   | Mixto: agilidad personal y colaboración humano-IA de la misma persona |
| liderazgo_ia  | T03 + T05   | Mixto: liderazgo y uso de IA del líder, frente a la IA de su equipo  |

Reglas del libro de diseño: solo filas con control OK; competencia con 2 de 3 ítems; resumen con 6 de 8
competencias; grupos con un mínimo de 5 personas; consulta individual con mínimo 1 solo para la propia
persona (o perfiles autorizados). No hay baremos, niveles A1–A5 ni índice global conjunto.
Todos los permisos se aplican aquí, en el backend.
"""
from __future__ import annotations

import json
import os
import sqlite3
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime

from .catalog import PULSE_GROUPS, SCALE_LABELS, Catalog, Test
from .scoring import CONTROL_OK, round_half_up

MIN_GROUP = max(5, int(os.environ.get("CDM_MIN_GROUP", "5")))
TODOS = "TODOS"

DASHBOARDS = {
    "persona": {"title": "Mi resultado · Agilidad personal", "label": "Persona", "tests": ["T01"], "individual": True,
                "subtitle": "Conoce tus competencias y planifica tu desarrollo"},
    "equipo": {"title": "Cuadro de mando · Equipo", "label": "Equipo", "tests": ["T02"], "individual": False,
               "subtitle": "Contribución individual al equipo, agregada sin exponer respuestas individuales"},
    "liderazgo": {"title": "Mi liderazgo · Propósito y autonomía", "label": "Liderazgo", "tests": ["T03"],
                  "individual": True, "leaders_only": True,
                  "subtitle": "Tu autopercepción junto a la percepción que recibes de tu equipo"},
    "organizacion": {"title": "Panel organizativo", "label": "Organización", "tests": ["T04"], "individual": False,
                     "subtitle": "Lectura ejecutiva con evidencia y respeto por el anonimato"},
    "ia": {"title": "IA transversal · Colaboración humano-IA", "label": "IA transversal", "tests": ["T05"],
           "individual": False, "subtitle": "Aumentar capacidades de forma útil, crítica, segura y responsable"},
    "persona_ia": {"title": "Persona + IA · Agilidad aumentada", "label": "Persona + IA", "tests": ["T01", "T05"],
                   "individual": True, "subtitle": "Tu agilidad personal y tu colaboración con la IA, lado a lado"},
    "liderazgo_ia": {"title": "Líder + IA · Liderar con agilidad aumentada", "label": "Líder + IA",
                     "tests": ["T03", "T05"], "individual": True, "leaders_only": True,
                     "subtitle": "Tu liderazgo, tu uso de la IA y la IA de tu equipo"},
}

# Puentes de lectura entre cuestionarios (propuesta descriptiva, no validada): (bloque A, bloque B, pregunta guía).
BRIDGES = {
    "persona_ia": [(4, 3, "Revisar supuestos y contrastar lo que propone la IA"),
                   (7, 2, "Practicar, iterar y aprender de los resultados de la IA"),
                   (5, 5, "Probar en pequeño cuando falta información"),
                   (6, 4, "Decidir qué hace la persona y qué apoya la IA"),
                   (2, 6, "Hacer una pausa antes de decidir con apoyo de IA"),
                   (8, 7, "Llevar lo aprendido a nuevas herramientas y datos")],
    "liderazgo_ia": [(3, 4, "Delegar en personas y en IA con responsabilidades explícitas"),
                     (5, 3, "Explorar alternativas contrastando lo que propone la IA"),
                     (6, 6, "Hablar con el equipo de errores y riesgos de la IA sin temor"),
                     (4, 2, "Revisar con el equipo cómo se está usando la IA"),
                     (7, 8, "Automatizar para liberar carga sin perder supervisión"),
                     (1, 1, "Conectar el uso de la IA con el propósito del equipo")],
}

NOTICES = {
    "persona": "Fortalezas y áreas son posiciones relativas dentro de tu perfil, no diagnósticos ni comparaciones con otras personas.",
    "equipo": "T02 describe la contribución individual al equipo. Su media resume autoinformes: no acredita funcionamiento "
              "colectivo, seguridad psicológica del equipo ni acuerdo entre miembros.",
    "liderazgo": "Autopercepción de liderazgo: no es una evaluación 360. Las tres preguntas del pulso sobre el responsable "
                 "son distintas de los ítems T03, así que no se calcula una brecha entre ambas fuentes.",
    "organizacion": "Cada perfil usa su propio n. No existe un índice global conjunto ni una puntuación de madurez.",
    "ia": "T05 usa una escala numérica 1–5 con anclajes verbales pendientes en el maestro. No infieras impacto real en "
          "productividad desde este autoinforme.",
    "persona_ia": "Las dos medias proceden de cuestionarios distintos (T01 y T05): se muestran juntas, nunca se suman ni "
                  "se restan. Los puentes de lectura son una propuesta para conversar, no una relación validada.",
    "liderazgo_ia": "T03 es autopercepción de liderazgo y T05 autoinforme de IA. La IA del equipo procede de otras personas "
                    "y se muestra solo con un mínimo de 5. Los puentes de lectura no son una relación validada.",
}

DISCLAIMER = ("Instrumento piloto · pendiente de validación · resultados para el desarrollo, no para selección, "
              "promoción ni despido.")


class Forbidden(Exception):
    pass


class BadRequest(Exception):
    pass


# ---------------------------------------------------------------- permisos

ROLE_DASHBOARDS = {
    "admin": set(DASHBOARDS),
    "consultor": set(DASHBOARDS),
    "rrhh": set(DASHBOARDS),
    "lider": {"persona", "persona_ia", "liderazgo", "liderazgo_ia", "equipo", "ia"},
    "participante": {"persona", "persona_ia"},
}

ROLE_LABELS = {"admin": "Administración", "consultor": "Consultor", "rrhh": "RRHH · solo lectura",
               "lider": "Líder", "participante": "Participante", "gestor": "Gestor de test"}


@dataclass
class Scope:
    staff_id: int
    email: str
    name: str
    role: str
    persona_id: str | None = None
    org_ids: set[str] | None = None          # None = todas
    team_id: str | None = None               # equipo propio (líder / participante)

    @property
    def dashboards(self) -> set[str]:
        return ROLE_DASHBOARDS.get(self.role, set())

    @property
    def can_pick_person(self) -> bool:
        return self.role in ("admin", "consultor")

    @property
    def can_export_data(self) -> bool:
        return self.role == "admin"

    @property
    def can_import(self) -> bool:
        return self.role == "admin"

    def can_edit_plan(self, key: str, f: "Filters") -> bool:
        if self.role in ("admin", "consultor"):
            return True
        if self.role == "rrhh":
            return key == "organizacion"
        if self.role in ("lider", "participante"):
            if DASHBOARDS[key]["individual"]:
                return f.persona == self.persona_id
            return self.role == "lider" and f.equipo == self.team_id
        return False


def scope_for(conn: sqlite3.Connection, staff_id: int) -> Scope:
    s = conn.execute("SELECT * FROM staff_user WHERE id = ?", (staff_id,)).fetchone()
    if s is None:
        raise Forbidden("Usuario no encontrado.")
    if s["role"] == "gestor":
        raise Forbidden("El rol Gestor de test no tiene acceso a los cuadros de mando.")
    scope = Scope(staff_id=s["id"], email=s["email"], name=s["name"], role=s["role"], persona_id=s["persona_id"])
    if s["role"] == "consultor":
        scope.org_ids = {r["organization_id"] for r in conn.execute(
            "SELECT organization_id FROM staff_org_access WHERE staff_id = ?", (staff_id,))}
    elif s["role"] in ("rrhh", "lider", "participante"):
        scope.org_ids = {s["organization_id"]} if s["organization_id"] else set()
    if s["persona_id"]:
        p = conn.execute("SELECT * FROM person WHERE id = ?", (s["persona_id"],)).fetchone()
        if p:
            scope.team_id = p["team_id"]
    return scope


# ---------------------------------------------------------------- filtros

@dataclass
class Filters:
    tipo: str = "DEMO"
    periodo: str = ""
    organizacion: str = TODOS
    equipo: str = TODOS
    persona: str = TODOS
    org_ids: list[str] | None = None      # restricción de alcance cuando organizacion = TODOS
    locked: list[str] = field(default_factory=list)

    @property
    def individual(self) -> bool:
        return self.persona != TODOS

    @property
    def key(self) -> str:
        return "|".join([self.tipo, self.periodo, self.organizacion, self.equipo, self.persona])

    def public(self) -> dict:
        return {"tipo": self.tipo, "periodo": self.periodo, "organizacion": self.organizacion, "equipo": self.equipo,
                "persona": self.persona, "locked": self.locked}


def periods(conn: sqlite3.Connection, tipo: str) -> list[str]:
    rows = conn.execute("SELECT DISTINCT periodo FROM evaluation WHERE tipo_datos = ? AND control = 'OK' "
                        "UNION SELECT DISTINCT periodo FROM pulse WHERE tipo_datos = ? AND control = 'OK' "
                        "ORDER BY periodo DESC", (tipo, tipo)).fetchall()
    return [r[0] for r in rows if r[0]]


def resolve_filters(conn: sqlite3.Connection, scope: Scope, key: str, raw: dict) -> Filters:
    if key not in DASHBOARDS:
        raise BadRequest("Cuadro de mando desconocido.")
    if key not in scope.dashboards:
        raise Forbidden("Tu rol no incluye este cuadro de mando.")
    spec = DASHBOARDS[key]
    tipo = (raw.get("tipo") or "DEMO").upper()
    if tipo not in ("REAL", "DEMO"):
        raise BadRequest("Tipo de datos no válido: usa REAL o DEMO (nunca se combinan).")
    f = Filters(tipo=tipo, periodo=raw.get("periodo") or "", organizacion=raw.get("organizacion") or TODOS,
                equipo=raw.get("equipo") or TODOS, persona=raw.get("persona") or TODOS)
    if not f.periodo:
        ps = periods(conn, tipo)
        f.periodo = ps[0] if ps else ""

    # Organización
    if scope.org_ids is not None:
        if f.organizacion != TODOS and f.organizacion not in scope.org_ids:
            raise Forbidden("Organización no autorizada para tu rol.")
        if f.organizacion == TODOS:
            if len(scope.org_ids) == 1:
                f.organizacion = next(iter(scope.org_ids))
            else:
                f.org_ids = sorted(scope.org_ids)
        if scope.role in ("rrhh", "lider", "participante"):
            f.locked.append("organizacion")

    # Equipo coherente con la organización
    if f.equipo != TODOS:
        t = conn.execute("SELECT organization_id FROM team WHERE id = ?", (f.equipo,)).fetchone()
        if t is None:
            raise BadRequest("Equipo desconocido.")
        if f.organizacion != TODOS and t["organization_id"] != f.organizacion:
            raise BadRequest("El equipo no pertenece a la organización elegida.")
        if scope.org_ids is not None and t["organization_id"] not in scope.org_ids:
            raise Forbidden("Equipo no autorizado para tu rol.")

    # Persona
    if not spec["individual"]:
        f.persona = TODOS
        f.locked.append("persona")
    if scope.role in ("lider", "participante"):
        if spec["individual"]:
            if f.persona not in (TODOS, scope.persona_id):
                raise Forbidden("Solo puedes consultar tu propio resultado.")
            f.persona = scope.persona_id
            f.locked += ["persona", "equipo"]
            f.equipo = TODOS
        else:   # líder en equipo / IA: su propio equipo, agregado
            if f.equipo not in (TODOS, scope.team_id):
                raise Forbidden("Solo puedes consultar tu propio equipo.")
            f.equipo = scope.team_id
            f.locked.append("equipo")
    elif scope.role == "rrhh" and spec["individual"]:
        if f.persona != TODOS:
            raise Forbidden("RRHH solo consulta resultados agregados, sin datos individuales.")
        f.locked.append("persona")
    if f.persona != TODOS:
        p = conn.execute("SELECT * FROM person WHERE id = ?", (f.persona,)).fetchone()
        if p is None:
            raise BadRequest("Persona desconocida.")
        if scope.org_ids is not None and p["organization_id"] not in scope.org_ids:
            raise Forbidden("Persona fuera de tu alcance.")
        if spec.get("leaders_only") and not p["is_leader"]:
            raise BadRequest("Esta persona no tiene rol de liderazgo registrado.")
        f.organizacion, f.equipo = p["organization_id"], TODOS
    return f


def options(conn: sqlite3.Connection, scope: Scope, key: str, f: Filters) -> dict:
    spec = DASHBOARDS[key]
    orgs = [dict(r) for r in conn.execute("SELECT id, name FROM organization ORDER BY name")
            if scope.org_ids is None or r["id"] in scope.org_ids]
    org_filter = [f.organizacion] if f.organizacion != TODOS else [o["id"] for o in orgs]
    q = ",".join("?" * len(org_filter)) or "''"
    teams = [dict(r) for r in conn.execute(
        f"SELECT t.id, t.name, t.organization_id, COUNT(p.id) AS census FROM team t LEFT JOIN person p ON p.team_id = t.id "
        f"WHERE t.organization_id IN ({q}) GROUP BY t.id ORDER BY t.organization_id, t.name", org_filter)]
    people = []
    if spec["individual"] and (scope.can_pick_person or scope.role in ("lider", "participante")):
        sql = (f"SELECT p.id, p.team_id, t.name AS team, p.is_leader FROM person p JOIN team t ON t.id = p.team_id "
               f"WHERE p.organization_id IN ({q})")
        if spec.get("leaders_only"):
            sql += " AND p.is_leader = 1"
        people = [dict(r) for r in conn.execute(sql + " ORDER BY p.id", org_filter)]
        if scope.role in ("lider", "participante"):
            people = [p for p in people if p["id"] == scope.persona_id]
    return {"tipos": ["DEMO", "REAL"], "periodos": periods(conn, f.tipo), "organizaciones": orgs, "equipos": teams,
            "personas": people}


# ---------------------------------------------------------------- consultas

def _cut_where(f: Filters, alias: str, persona_col: str = "persona_id", persona_ids: list[str] | None = None,
               skip_periodo: bool = False) -> tuple[str, list]:
    c, p = [f"{alias}.tipo_datos = ?", f"{alias}.control = 'OK'"], [f.tipo]
    if not skip_periodo:
        c.append(f"{alias}.periodo = ?")
        p.append(f.periodo)
    if f.organizacion != TODOS:
        c.append(f"{alias}.organizacion_id = ?")
        p.append(f.organizacion)
    elif f.org_ids is not None:
        c.append(f"{alias}.organizacion_id IN ({','.join('?' * len(f.org_ids)) or chr(39) * 2})")
        p += f.org_ids
    if f.equipo != TODOS:
        c.append(f"{alias}.equipo_id = ?")
        p.append(f.equipo)
    if persona_ids is not None:
        c.append(f"{alias}.{persona_col} IN ({','.join('?' * len(persona_ids)) or chr(39) * 2})")
        p += persona_ids
    elif f.persona != TODOS:
        c.append(f"{alias}.{persona_col} = ?")
        p.append(f.persona)
    return " AND ".join(c), p


def fetch_evals(conn: sqlite3.Connection, test: Test, f: Filters, persona_ids: list[str] | None = None,
                skip_periodo: bool = False) -> list[dict]:
    """Filas incluidas en el cuadro: control OK, al menos una respuesta válida y dentro de los filtros."""
    where, params = _cut_where(f, "e", persona_ids=persona_ids, skip_periodo=skip_periodo)
    rows = conn.execute(f"SELECT e.* FROM evaluation e WHERE e.test_code = ? AND {where}", [test.code] + params).fetchall()
    if not rows:
        return []
    ids = [r["id"] for r in rows]
    blocks: dict[int, dict[int, float | None]] = defaultdict(dict)
    valid: Counter = Counter()
    answers: dict[int, dict[str, str]] = defaultdict(dict)
    for start in range(0, len(ids), 500):
        chunk = ids[start:start + 500]
        q = ",".join("?" * len(chunk))
        for b in conn.execute(f"SELECT * FROM block_score WHERE eval_id IN ({q})", chunk):
            blocks[b["eval_id"]][b["block"]] = b["score"]
            valid[b["eval_id"]] += b["n_valid"]
        for a in conn.execute(f"SELECT * FROM answer WHERE eval_id IN ({q})", chunk):
            answers[a["eval_id"]][a["item_id"]] = a["raw"]
    return [dict(r) | {"blocks": blocks[r["id"]], "answers": answers[r["id"]]} for r in rows if valid[r["id"]] > 0]


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _r(x, d=2):
    return round_half_up(x, d) if x is not None else None


def profile(test: Test, rows: list[dict], min_n: int) -> dict:
    """Medias descriptivas por competencia (bloque) y resumen, con supresión por muestra mínima."""
    U = len(rows)
    blocks = []
    for b in test.blocks:
        vals = [r["blocks"].get(b["idx"]) for r in rows if r["blocks"].get(b["idx"]) is not None]
        n = len(vals)
        ok = n >= min_n and n > 0
        blocks.append({"idx": b["idx"], "name": b["name"], "short": b["short"], "n": n,
                       "mean": _r(_mean(vals)) if ok else None,
                       "sd": _r(statistics.pstdev(vals)) if ok and n > 1 else None,
                       "coverage": round(n / U, 3) if U else None,
                       "suppressed": n > 0 and not ok})
    medias = [r["media_descriptiva"] for r in rows if r["media_descriptiva"] is not None]
    summary_ok = len(medias) >= min_n and medias
    if U == 0:
        status = "SIN DATOS"
    elif U < min_n:
        status = "MUESTRA INSUFICIENTE"
    else:
        status = "PERFIL DISPONIBLE"
    means = [b for b in blocks if b["mean"] is not None]
    ranked = sorted(means, key=lambda b: (-b["mean"], b["idx"]))
    k = 2 if len(ranked) >= 4 else 1
    strengths = ranked[:k] if len(ranked) >= 2 else []
    areas = sorted(ranked[-k:], key=lambda b: b["mean"]) if len(ranked) >= 2 else []
    return {"test": test.code, "name": test.name, "version": test.version, "scale_id": test.scale_id,
            "n": U, "min_n": min_n, "status": status, "blocks": blocks,
            "media": _r(_mean(medias)) if summary_ok else None, "n_media": len(medias),
            "blocks_calculated": len(means),
            "strengths": [{"idx": b["idx"], "name": b["name"], "mean": b["mean"]} for b in strengths],
            "areas": [{"idx": b["idx"], "name": b["name"], "mean": b["mean"]} for b in areas]}


def item_detail(test: Test, row: dict) -> list[dict]:
    """Respuestas ítem a ítem de una persona (solo consulta individual autorizada)."""
    out = []
    for b in test.blocks:
        items = []
        for iid in b["items"]:
            it = next(i for i in test.items if i.item_id == iid)
            raw = row["answers"].get(iid)
            items.append({"item_id": iid, "text": it.text, "value": int(raw) if raw and raw.isdigit() else None,
                          "nv": raw == "NV", "omitted": raw is None})
        out.append({"idx": b["idx"], "short": b["short"], "score": _r(row["blocks"].get(b["idx"])), "items": items})
    return out


def item_means(test: Test, rows: list[dict], min_n: int) -> list[dict]:
    out = []
    for it in test.active_items:
        vals = [int(r["answers"][it.item_id]) for r in rows if (r["answers"].get(it.item_id) or "").isdigit()]
        if len(vals) >= min_n:
            out.append({"item_id": it.item_id, "text": it.text, "block": it.block, "mean": _r(_mean(vals)), "n": len(vals)})
    return out


def distribution(test: Test, rows: list[dict], min_n: int) -> dict:
    """Personas por media redondeada de cada competencia (1–5): mapa de calor de 'cómo responde el grupo'."""
    out = []
    for b in test.blocks:
        vals = [r["blocks"].get(b["idx"]) for r in rows if r["blocks"].get(b["idx"]) is not None]
        counts = Counter(int(round_half_up(v, 0)) for v in vals)
        out.append({"idx": b["idx"], "short": b["short"], "n": len(vals),
                    "counts": [counts.get(k, 0) for k in range(1, 6)] if len(vals) >= min_n else None})
    return {"rows": out, "labels": [SCALE_LABELS.get(test.scale_id, {}).get(k, str(k)) for k in range(1, 6)]}


def fetch_pulse(conn: sqlite3.Connection, f: Filters, by_responsable: bool = False,
                persona_ids: list[str] | None = None) -> list[dict]:
    where, params = _cut_where(f, "p", persona_col="responsable_id" if by_responsable else "persona_id",
                               persona_ids=persona_ids)
    if by_responsable and f.persona != TODOS:
        # Las personas del equipo de un líder pueden estar en otro equipo_id: el filtro es responsable_id.
        where = where.replace("p.equipo_id = ? AND ", "")
    rows = conn.execute(f"SELECT p.* FROM pulse p WHERE {where}", params).fetchall()
    if not rows:
        return []
    ids = [r["id"] for r in rows]
    answers: dict[int, dict[str, str]] = defaultdict(dict)
    for start in range(0, len(ids), 500):
        chunk = ids[start:start + 500]
        for a in conn.execute(f"SELECT * FROM pulse_answer WHERE pulse_id IN ({','.join('?' * len(chunk))})", chunk):
            answers[a["pulse_id"]][a["item_id"]] = a["raw"]
    out = []
    for r in rows:
        nums = {k: int(v) for k, v in answers[r["id"]].items() if v.isdigit()}
        if nums:
            out.append(dict(r) | {"values": nums})
    return out


def pulse_summary(catalog: Catalog, rows: list[dict], min_items: int, min_enps: int = MIN_GROUP) -> dict:
    items = {}
    for p in catalog.pulse:
        if p.item_id == "ENPS":
            continue
        vals = [r["values"][p.item_id] for r in rows if p.minimo <= r["values"].get(p.item_id, -1) <= p.maximo]
        need = MIN_GROUP if p.item_id.startswith("L") else min_items
        items[p.item_id] = {"short": p.short, "text": p.text, "component": p.component, "n": len(vals),
                            "mean": _r(_mean(vals)) if len(vals) >= need and vals else None,
                            "suppressed": 0 < len(vals) < need}
    enps_vals = [r["values"]["ENPS"] for r in rows if "ENPS" in r["values"]]
    n = len(enps_vals)
    enps = {"n": n, "min_n": min_enps, "score": None, "promoters": None, "passives": None, "detractors": None}
    if n >= min_enps:
        pro = sum(1 for v in enps_vals if v >= 9)
        det = sum(1 for v in enps_vals if v <= 6)
        enps |= {"score": _r(100 * (pro - det) / n, 1), "promoters": pro, "passives": n - pro - det, "detractors": det}
    return {"n": len(rows), "items": items, "groups": PULSE_GROUPS, "enps": enps, "min_items": min_items}


def evolution(conn: sqlite3.Connection, test: Test, f: Filters, min_n: int, persona_ids: list[str] | None = None) -> dict:
    """Media descriptiva por periodo: solo mediciones comparables (misma versión) y con muestra suficiente."""
    rows = fetch_evals(conn, test, f, persona_ids=persona_ids, skip_periodo=True)
    by_period: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r["test_version"] == test.version and r["media_descriptiva"] is not None:
            by_period[r["periodo"]].append(r["media_descriptiva"])
    series = [{"periodo": p, "n": len(v), "mean": _r(_mean(v)) if len(v) >= min_n else None,
               "suppressed": len(v) < min_n} for p, v in sorted(by_period.items())]
    valid = [s for s in series if s["mean"] is not None]
    reason = None
    if len(valid) < 2:
        reason = ("Esta es la línea base. La comparación aparecerá cuando exista una segunda medición compatible "
                  "con muestra suficiente.")
    return {"test": test.code, "version": test.version, "series": series, "available": len(valid) >= 2, "reason": reason}


def quality(conn: sqlite3.Connection, tests: list[str], f: Filters) -> dict:
    """Estado de control de la captura en el corte (en consulta individual, solo las de esa persona)."""
    out = {}
    org_clause, params = "", [f.tipo, f.periodo]
    if f.organizacion != TODOS:
        org_clause = " AND organizacion_id = ?"
        params.append(f.organizacion)
    elif f.org_ids is not None:
        org_clause = f" AND organizacion_id IN ({','.join('?' * len(f.org_ids)) or chr(39) * 2})"
        params += f.org_ids
    if f.persona != TODOS:
        # Consulta individual: solo las capturas de esa persona, nunca recuentos de su organización.
        org_clause += " AND persona_id = ?"
        params.append(f.persona)
    for code in tests:
        rows = conn.execute(f"SELECT control, COUNT(*) n FROM evaluation WHERE test_code = ? AND tipo_datos = ? "
                            f"AND periodo = ?{org_clause} GROUP BY control", [code] + params).fetchall()
        out[code] = {r["control"]: r["n"] for r in rows}
    rows = conn.execute(f"SELECT control, COUNT(*) n FROM pulse WHERE tipo_datos = ? AND periodo = ?{org_clause} "
                        f"GROUP BY control", params).fetchall()
    out["PULSO"] = {r["control"]: r["n"] for r in rows}
    return out


def census(conn: sqlite3.Connection, f: Filters, persona_ids: list[str] | None = None) -> int:
    if persona_ids is not None:
        return len(persona_ids)
    sql, params = "SELECT COUNT(*) FROM person WHERE 1=1", []
    if f.organizacion != TODOS:
        sql += " AND organization_id = ?"
        params.append(f.organizacion)
    elif f.org_ids is not None:
        sql += f" AND organization_id IN ({','.join('?' * len(f.org_ids)) or chr(39) * 2})"
        params += f.org_ids
    if f.equipo != TODOS:
        sql += " AND team_id = ?"
        params.append(f.equipo)
    return conn.execute(sql, params).fetchone()[0]


def by_team(conn: sqlite3.Connection, test: Test, f: Filters, min_n: int) -> list[dict]:
    """Medias por equipo dentro del alcance: solo se publican equipos con muestra suficiente."""
    rows = fetch_evals(conn, test, Filters(tipo=f.tipo, periodo=f.periodo, organizacion=f.organizacion,
                                           org_ids=f.org_ids), )
    names = {r["id"]: r["name"] for r in conn.execute("SELECT id, name FROM team")}
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["equipo_id"]].append(r)
    out = []
    for team_id, rr in sorted(groups.items(), key=lambda kv: names.get(kv[0], kv[0])):
        p = profile(test, rr, min_n)
        visible = len(rr) >= min_n
        out.append({"team_id": team_id, "team": names.get(team_id, team_id), "n": len(rr), "visible": visible,
                    "media": p["media"] if visible else None,
                    "blocks": [b["mean"] for b in p["blocks"]] if visible else None})
    return out


def team_members(conn: sqlite3.Connection, leader_id: str) -> list[str]:
    return [r[0] for r in conn.execute("SELECT id FROM person WHERE responsable_id = ?", (leader_id,))]


# ---------------------------------------------------------------- cuadros

def _kpi(value, label, sub="", fmt="mean", tone=None):
    return {"value": value, "label": label, "sub": sub, "fmt": fmt, "tone": tone}


def build(conn: sqlite3.Connection, catalog: Catalog, scope: Scope, key: str, f: Filters,
          now: datetime | None = None) -> dict:
    spec = DASHBOARDS[key]
    tests = [catalog.tests[c] for c in spec["tests"]]
    individual = f.individual
    min_n = 1 if individual else MIN_GROUP
    rows = {t.code: fetch_evals(conn, t, f) for t in tests}
    profiles = {t.code: profile(t, rows[t.code], min_n) for t in tests}
    show_items = individual and (scope.can_pick_person or f.persona == scope.persona_id)

    # Pulso: en los cuadros de liderazgo, el filtro de persona selecciona responsable_id (equipo del líder).
    leader_view = key in ("liderazgo", "liderazgo_ia")
    if leader_view and individual:
        pulse_rows = fetch_pulse(conn, f, by_responsable=True)
        pulse = pulse_summary(catalog, pulse_rows, MIN_GROUP)
        pulse["source"] = "Pulso de las personas que reportan a este líder"
    else:
        pulse_rows = fetch_pulse(conn, f)
        pulse = pulse_summary(catalog, pulse_rows, 1 if individual else MIN_GROUP)
        pulse["source"] = "Tu pulso de experiencia laboral" if individual else "Pulso de experiencia laboral del grupo"

    out = {
        "key": key,
        "dashboard": {"key": key, "title": spec["title"], "subtitle": spec["subtitle"], "label": spec["label"],
                      "tests": [{"code": t.code, "name": t.name, "version": t.version, "scale_id": t.scale_id,
                                 "subtitle": t.subtitle, "items": len(t.active_items)} for t in tests]},
        "generated_at": (now or datetime.now()).isoformat(timespec="seconds"),
        "filters": f.public(),
        "individual": individual,
        "min_group": MIN_GROUP,
        "min_n": min_n,
        "profiles": profiles,
        "pulse": pulse,
        "evolution": {t.code: evolution(conn, t, f, min_n) for t in tests},
        "quality": quality(conn, spec["tests"], f),
        "notice": NOTICES[key],
        "disclaimer": DISCLAIMER,
        "scale_labels": {t.code: SCALE_LABELS.get(t.scale_id, {}) for t in tests},
        "extras": {},
        "plan": plan_get(conn, key, f) | {"editable": scope.can_edit_plan(key, f)},
    }
    if show_items:
        out["extras"]["items"] = {t.code: item_detail(t, rows[t.code][0]) for t in tests if rows[t.code]}
    n_census = census(conn, f) if not individual else 1
    builder = globals()[f"_build_{key}"]
    builder(conn, catalog, out, tests, rows, f, n_census)
    return out


def _participation_kpi(n, total, label="Personas con datos válidos"):
    pct = n / total if total else None
    return _kpi(n, label, f"de {total} en el censo" + (f" · {round(pct * 100)} %" if pct is not None else ""), "int")


def _build_persona(conn, catalog, out, tests, rows, f, n_census):
    t = tests[0]
    p = out["profiles"][t.code]
    answered = sum(1 for r in rows[t.code] for v in r["answers"].values() if v.isdigit())
    nv = sum(1 for r in rows[t.code] for v in r["answers"].values() if v == "NV")
    if out["individual"]:
        out["kpis"] = [_kpi(len(t.active_items), "Ítems previstos", f"{answered} respondidos · {nv} «no observable»", "int"),
                       _kpi(p["blocks_calculated"], "Competencias calculadas", "de 8 · mínimo 2 de 3 ítems por competencia",
                            "frac8"),
                       _kpi(p["media"], "Media descriptiva", "escala 1–5 · requiere 6 de 8 competencias"),
                       _kpi(p["status"], "Estado de la selección", f"Persona {f.persona}", "text")]
    else:
        out["kpis"] = [_participation_kpi(p["n"], n_census),
                       _kpi(p["media"], "Media descriptiva", f"n = {p['n_media']} con resumen"),
                       _kpi(p["blocks_calculated"], "Competencias publicadas", f"mínimo {out['min_group']} personas", "frac8"),
                       _kpi(p["status"], "Estado de la selección", "", "text")]
    out["extras"]["nv"] = {"answered": answered, "nv": nv}


def _build_equipo(conn, catalog, out, tests, rows, f, n_census):
    t = tests[0]
    p = out["profiles"][t.code]
    sds = [b["sd"] for b in p["blocks"] if b["sd"] is not None]
    enps = out["pulse"]["enps"]
    out["kpis"] = [_participation_kpi(p["n"], n_census, "Personas del equipo con datos"),
                   _kpi(p["media"], "Media descriptiva T02", "8 competencias · 24 ítems"),
                   _kpi(_r(_mean(sds)), "Dispersión entre personas", "desviación típica media dentro de las competencias"),
                   _kpi(enps["score"], "eNPS del equipo", f"n = {enps['n']} · aparte del modelo", "enps")]
    out["extras"]["distribution"] = distribution(t, rows[t.code], MIN_GROUP)
    out["extras"]["agreement"] = [{"short": b["short"], "mean": b["mean"], "sd": b["sd"]} for b in p["blocks"]
                                  if b["mean"] is not None and b["sd"] is not None]
    # Comparación con la organización (marca): solo si se mira un equipo concreto.
    if f.equipo != TODOS:
        org_f = Filters(tipo=f.tipo, periodo=f.periodo, organizacion=f.organizacion, org_ids=f.org_ids)
        org_p = profile(t, fetch_evals(conn, t, org_f), MIN_GROUP)
        out["extras"]["reference"] = {"label": "Media de la organización", "blocks": [b["mean"] for b in org_p["blocks"]],
                                      "n": org_p["n"]}
    out["extras"]["participation"] = {"census": n_census, "responded": p["n"], "min_group": MIN_GROUP}


def _build_liderazgo(conn, catalog, out, tests, rows, f, n_census):
    t = tests[0]
    p = out["profiles"][t.code]
    pulse = out["pulse"]
    lead = [pulse["items"][k] for k in PULSE_GROUPS["responsable"]]
    informants = max((i["n"] for i in lead), default=0)
    if out["individual"]:
        team_n = len(team_members(conn, f.persona))
        sources = 1 + (1 if any(i["mean"] is not None for i in lead) else 0)
        out["kpis"] = [_kpi(p["media"], "Mi autopercepción", "T03 · 8 competencias · 24 ítems"),
                       _kpi(_r(_mean([i["mean"] for i in lead])), "Percepción del equipo",
                            f"{informants} de {team_n} personas · umbral de anonimato {out['min_group']}"),
                       _kpi(pulse["enps"]["score"], "eNPS de mi equipo", f"n = {pulse['enps']['n']}", "enps"),
                       _kpi(f"{sources} de 3", "Fuentes disponibles", "autoevaluación · equipo · 360 pendiente", "text")]
        hi = p["strengths"][0]["idx"] if p["strengths"] else None
        lo = p["areas"][0]["idx"] if p["areas"] else None
        blocks = {b["idx"]: b for b in t.blocks}
        texts = {i.item_id: i.text for i in t.items}
        out["extras"]["conversations"] = {
            "practice": [texts[i] for i in blocks[hi]["items"]] if hi else [],
            "explore": [texts[i] for i in blocks[lo]["items"]] if lo else [],
            "explore_block": blocks[lo]["name"] if lo else None, "practice_block": blocks[hi]["name"] if hi else None}
    else:
        out["kpis"] = [_participation_kpi(p["n"], conn.execute(
                           "SELECT COUNT(*) FROM person WHERE is_leader = 1" + (" AND organization_id = ?" if f.organizacion != TODOS else ""),
                           [f.organizacion] if f.organizacion != TODOS else []).fetchone()[0], "Líderes con datos"),
                       _kpi(p["media"], "Autopercepción media", "T03 · líderes del alcance"),
                       _kpi(_r(_mean([i["mean"] for i in lead])), "Percepción del responsable",
                            "L01–L03 · pulso del grupo"),
                       _kpi(p["status"], "Estado de la selección", "", "text")]
    out["extras"]["received"] = lead
    out["extras"]["sources"] = [
        {"label": "AUTO", "value": f"n = {p['n']}", "text": "Autoevaluación T03"},
        {"label": "EQUIPO", "value": f"n = {informants}",
         "text": "Supera el umbral de anonimato" if informants >= out["min_group"] else
         f"Por debajo del umbral de anonimato ({out['min_group']}): oculto"},
        {"label": "360", "value": "pendiente", "text": "Estructura futura sin validar: no se administra"},
        {"label": "COMBINADO", "value": "no aplicado", "text": "Sin pesos aprobados: las fuentes se muestran por separado"}]


def _build_organizacion(conn, catalog, out, tests, rows, f, n_census):
    t = tests[0]
    p = out["profiles"][t.code]
    teams = by_team(conn, t, f, MIN_GROUP)
    enps = out["pulse"]["enps"]
    out["kpis"] = [_participation_kpi(p["n"], n_census, "Participación T04"),
                   _kpi(enps["score"], "eNPS", f"n = {enps['n']} · aparte de las puntuaciones", "enps"),
                   _kpi(p["media"], "Media descriptiva T04", "8 competencias · 24 ítems"),
                   _kpi(f"{sum(1 for x in teams if x['visible'])} de {len(teams)}", "Equipos con resultados",
                        f"superan el umbral de anonimato ({MIN_GROUP})", "text")]
    five = []
    for code, test in catalog.tests.items():
        rr = fetch_evals(conn, test, f)
        medias = [r["media_descriptiva"] for r in rr if r["media_descriptiva"] is not None]
        five.append({"test": code, "name": test.name, "n_data": len(rr), "n_summary": len(medias),
                     "media": _r(_mean(medias)) if len(medias) >= MIN_GROUP else None})
    out["extras"]["five_profiles"] = five
    out["extras"]["teams"] = {"blocks": [b["short"] for b in t.blocks], "rows": teams}
    ranked = sorted([b for b in p["blocks"] if b["mean"] is not None], key=lambda b: b["mean"])
    out["extras"]["priorities"] = [{"name": b["name"], "mean": b["mean"]} for b in ranked[:3]]


def _build_ia(conn, catalog, out, tests, rows, f, n_census):
    t = tests[0]
    p = out["profiles"][t.code]
    means = [b for b in p["blocks"] if b["mean"] is not None]
    hi = max(means, key=lambda b: b["mean"]) if means else None
    lo = min(means, key=lambda b: b["mean"]) if means else None
    out["kpis"] = [_kpi(p["media"], "Media descriptiva T05", "IA transversal · 8 competencias"),
                   _participation_kpi(p["n"], n_census),
                   _kpi(hi["mean"] if hi else None, "Competencia más alta", hi["name"] if hi else "sin datos suficientes"),
                   _kpi(lo["mean"] if lo else None, "Competencia más baja", lo["name"] if lo else "sin datos suficientes")]
    out["extras"]["teams"] = {"rows": by_team(conn, t, f, MIN_GROUP)}
    im = sorted(item_means(t, rows[t.code], MIN_GROUP), key=lambda x: -x["mean"])
    out["extras"]["behaviours"] = {"top": im[:3], "bottom": sorted(im[-3:], key=lambda x: x["mean"]) if len(im) >= 6 else []}


def _bridges(key, profiles, a, b):
    pa = {x["idx"]: x for x in profiles[a]["blocks"]}
    pb = {x["idx"]: x for x in profiles[b]["blocks"]}
    return [{"a": {"test": a, "name": pa[i]["name"], "short": pa[i]["short"], "mean": pa[i]["mean"]},
             "b": {"test": b, "name": pb[j]["name"], "short": pb[j]["short"], "mean": pb[j]["mean"]},
             "prompt": text} for i, j, text in BRIDGES[key]]


def _combined(profiles, codes):
    allb = [(b["mean"], code, b["name"]) for code in codes for b in profiles[code]["blocks"] if b["mean"] is not None]
    allb.sort(key=lambda x: -x[0])
    if len(allb) < 4:
        return [], []
    top = [{"test": c, "name": n, "mean": m} for m, c, n in allb[:3]]
    low = [{"test": c, "name": n, "mean": m} for m, c, n in sorted(allb[-3:])]
    return top, low


def _build_persona_ia(conn, catalog, out, tests, rows, f, n_census):
    a, b = (t.code for t in tests)
    pa, pb = out["profiles"][a], out["profiles"][b]
    if out["individual"]:
        both = "Sí" if rows[a] and rows[b] else "No"
        out["kpis"] = [_kpi(pa["media"], "Agilidad personal · T01", f"{pa['blocks_calculated']} de 8 competencias"),
                       _kpi(pb["media"], "Colaboración humano-IA · T05", f"{pb['blocks_calculated']} de 8 competencias"),
                       _kpi(pa["blocks_calculated"] + pb["blocks_calculated"], "Competencias calculadas", "de 16 en total",
                            "frac16"),
                       _kpi(both, "Ambos cuestionarios", "misma persona y periodo", "text")]
    else:
        ids_a = {r["persona_id"] for r in rows[a]}
        ids_b = {r["persona_id"] for r in rows[b]}
        out["kpis"] = [_kpi(pa["media"], "Agilidad personal · T01", f"n = {pa['n_media']}"),
                       _kpi(pb["media"], "Colaboración humano-IA · T05", f"n = {pb['n_media']}"),
                       _participation_kpi(len(ids_a & ids_b), n_census, "Personas con ambos"),
                       _kpi(pa["blocks_calculated"] + pb["blocks_calculated"], "Competencias publicadas",
                            f"de 16 · mínimo {MIN_GROUP} personas", "frac16")]
    out["extras"]["bridges"] = _bridges("persona_ia", out["profiles"], a, b)
    out["extras"]["combined"] = dict(zip(("strengths", "areas"), _combined(out["profiles"], [a, b])))


def _build_liderazgo_ia(conn, catalog, out, tests, rows, f, n_census):
    a, b = (t.code for t in tests)
    t05 = catalog.tests[b]
    pa, pb = out["profiles"][a], out["profiles"][b]
    if out["individual"]:
        members = team_members(conn, f.persona)
        mf = Filters(tipo=f.tipo, periodo=f.periodo, organizacion=TODOS, org_ids=f.org_ids)
        team_p = profile(t05, fetch_evals(conn, t05, mf, persona_ids=members), MIN_GROUP)
        ref_label = "IA de mi equipo"
        team_sub = f"{team_p['n']} de {len(members)} personas · mínimo {MIN_GROUP}"
    else:
        others = [r[0] for r in conn.execute("SELECT id FROM person WHERE is_leader = 0")]
        team_p = profile(t05, fetch_evals(conn, t05, f, persona_ids=others), MIN_GROUP)
        ref_label = "IA de los equipos"
        team_sub = f"n = {team_p['n']} personas sin rol de liderazgo"
        # La IA de los líderes: T05 restringido a líderes (en vista agregada).
        leaders = [r[0] for r in conn.execute("SELECT id FROM person WHERE is_leader = 1")]
        out["profiles"][b] = pb = profile(t05, fetch_evals(conn, t05, f, persona_ids=leaders), MIN_GROUP)
        out["evolution"][b] = evolution(conn, t05, f, MIN_GROUP, persona_ids=leaders)
    lead = [out["pulse"]["items"][k] for k in PULSE_GROUPS["responsable"]]
    out["kpis"] = [_kpi(pa["media"], "Liderazgo · T03", "autopercepción" + ("" if out["individual"] else f" · n = {pa['n']}")),
                   _kpi(pb["media"], "Mi IA · T05" if out["individual"] else "IA de los líderes · T05",
                        f"{pb['blocks_calculated']} de 8 competencias"),
                   _kpi(team_p["media"], ref_label, team_sub),
                   _kpi(_r(_mean([i["mean"] for i in lead])), "Percepción del equipo", "L01–L03 · mínimo 5")]
    out["extras"]["bridges"] = _bridges("liderazgo_ia", out["profiles"], a, b)
    out["extras"]["reference"] = {"label": ref_label, "blocks": [x["mean"] for x in team_p["blocks"]], "n": team_p["n"],
                                  "test": b}
    out["extras"]["received"] = lead
    out["extras"]["combined"] = dict(zip(("strengths", "areas"), _combined(out["profiles"], [a, b])))


# ---------------------------------------------------------------- inicio y planes

def overview(conn: sqlite3.Connection, catalog: Catalog, scope: Scope, raw: dict) -> dict:
    cards = []
    for key, spec in DASHBOARDS.items():
        if key not in scope.dashboards:
            continue
        f = resolve_filters(conn, scope, key, {"tipo": raw.get("tipo"), "periodo": raw.get("periodo"),
                                               "organizacion": raw.get("organizacion")})
        min_n = 1 if f.individual else MIN_GROUP
        stats = []
        for code in spec["tests"]:
            p = profile(catalog.tests[code], fetch_evals(conn, catalog.tests[code], f), min_n)
            stats.append({"test": code, "name": catalog.tests[code].name, "n": p["n"], "media": p["media"],
                          "status": p["status"]})
        cards.append({"key": key, "label": spec["label"], "title": spec["title"], "subtitle": spec["subtitle"],
                      "tests": stats, "individual": f.individual})
    f0 = resolve_filters(conn, scope, next(iter(scope.dashboards)), raw) if scope.dashboards else None
    return {"cards": cards, "filters": f0.public() if f0 else {}, "periodos": periods(conn, f0.tipo if f0 else "DEMO"),
            "min_group": MIN_GROUP, "disclaimer": DISCLAIMER}


def plan_get(conn: sqlite3.Connection, key: str, f: Filters) -> dict:
    r = conn.execute("SELECT * FROM action_plan WHERE dashboard = ? AND scope_key = ?", (key, f.key)).fetchone()
    if r is None:
        return {"objetivo": "", "actions": [], "updated_by": None, "updated_at": None}
    return {"objetivo": r["objetivo"] or "", "actions": json.loads(r["actions"]), "updated_by": r["updated_by"],
            "updated_at": r["updated_at"]}


PLAN_STATES = ("Pendiente", "En curso", "Hecha")


def plan_save(conn: sqlite3.Connection, scope: Scope, key: str, f: Filters, body: dict) -> dict:
    if not scope.can_edit_plan(key, f):
        raise Forbidden("Tu rol no puede editar el plan de esta selección.")
    objetivo = str(body.get("objetivo") or "")[:500]
    actions = []
    for a in (body.get("actions") or [])[:6]:
        estado = a.get("estado") if a.get("estado") in PLAN_STATES else "Pendiente"
        actions.append({k: str(a.get(k) or "")[:300] for k in ("plazo", "accion", "responsable", "fecha_limite", "evidencia")}
                       | {"estado": estado})
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute("""INSERT INTO action_plan(dashboard, scope_key, objetivo, actions, updated_by, updated_at)
                    VALUES (?,?,?,?,?,?) ON CONFLICT(dashboard, scope_key) DO UPDATE SET
                    objetivo = excluded.objetivo, actions = excluded.actions, updated_by = excluded.updated_by,
                    updated_at = excluded.updated_at""",
                 (key, f.key, objetivo, json.dumps(actions, ensure_ascii=False), scope.email, now))
    conn.commit()
    return plan_get(conn, key, f)


def data_rows(conn: sqlite3.Connection, catalog: Catalog, scope: Scope, key: str, f: Filters) -> dict:
    """Filas con el formato Datos_Txx (exportación administrativa, ítem a ítem)."""
    if not scope.can_export_data:
        raise Forbidden("La exportación de datos ítem a ítem solo está autorizada a administración.")
    out = {}
    for code in DASHBOARDS[key]["tests"]:
        t = catalog.tests[code]
        where, params = _cut_where(Filters(tipo=f.tipo, periodo=f.periodo, organizacion=f.organizacion,
                                           equipo=f.equipo, persona=f.persona, org_ids=f.org_ids), "e")
        where = where.replace("e.control = 'OK'", "1=1")
        evs = conn.execute(f"SELECT * FROM evaluation e WHERE e.test_code = ? AND {where} ORDER BY persona_id",
                           [code] + params).fetchall()
        rows = []
        for e in evs:
            ans = {a["item_id"]: a["raw"] for a in conn.execute("SELECT * FROM answer WHERE eval_id = ?", (e["id"],))}
            bl = {b["block"]: b["score"] for b in conn.execute("SELECT * FROM block_score WHERE eval_id = ?", (e["id"],))}
            rows.append([e["evaluacion_id"], e["persona_id"], e["organizacion_id"], e["equipo_id"], e["periodo"],
                         e["tipo_datos"], e["fecha_iso"]]
                        + [ans.get(i.item_id, "") for i in t.active_items]
                        + [e["control"]] + [_r(bl.get(i)) for i in range(1, 9)] + [_r(e["media_descriptiva"])])
        out[code] = {"header": ["evaluacion_id", "persona_id", "organizacion_id", "equipo_id", "periodo", "tipo_datos",
                                "fecha_iso"] + [i.item_id for i in t.active_items] + ["control"]
                               + [f"bloque_{i}" for i in range(1, 9)] + ["media_descriptiva"], "rows": rows}
    return out


# ---------------------------------------------------------------- distribución personalizada

LAYOUT_SPANS = (3, 4, 6, 8, 9, 12)       # columnas de una rejilla de 12


def _layout_check(scope: Scope, key: str) -> None:
    if key not in DASHBOARDS:
        raise BadRequest("Cuadro de mando desconocido.")
    if key not in scope.dashboards:
        raise Forbidden("Tu rol no incluye este cuadro de mando.")


def layout_get(conn: sqlite3.Connection, scope: Scope, key: str) -> dict | None:
    _layout_check(scope, key)
    r = conn.execute("SELECT layout FROM user_layout WHERE staff_id = ? AND dashboard = ?", (scope.staff_id, key)).fetchone()
    return json.loads(r["layout"]) if r else None


def layout_save(conn: sqlite3.Connection, scope: Scope, key: str, body: dict) -> dict:
    """Guarda el orden, el ancho y los paneles ocultos. Los identificadores se validan por forma, no por contenido:
    un panel que no existe en una vista concreta simplemente se ignora al aplicar la distribución."""
    _layout_check(scope, key)
    ok_id = lambda v: isinstance(v, str) and 0 < len(v) <= 40 and all(c.isalnum() or c in "-_" for c in v)
    order = body.get("order") or []
    spans = body.get("spans") or {}
    hidden = body.get("hidden") or []
    if not (isinstance(order, list) and isinstance(spans, dict) and isinstance(hidden, list)):
        raise BadRequest("Distribución no válida.")
    if len(order) > 60 or len(spans) > 60 or len(hidden) > 60:
        raise BadRequest("Demasiados paneles en la distribución.")
    if not all(ok_id(v) for v in order + hidden + list(spans)):
        raise BadRequest("Identificador de panel no válido.")
    if any(v not in LAYOUT_SPANS for v in spans.values()):
        raise BadRequest("Ancho no válido: usa 3, 4, 6, 8, 9 o 12 columnas.")
    layout = {"order": list(dict.fromkeys(order)), "spans": spans, "hidden": sorted(set(hidden))}
    conn.execute("""INSERT INTO user_layout(staff_id, dashboard, layout, updated_at) VALUES (?,?,?,?)
                    ON CONFLICT(staff_id, dashboard) DO UPDATE SET layout = excluded.layout, updated_at = excluded.updated_at""",
                 (scope.staff_id, key, json.dumps(layout), datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    return layout


def layout_reset(conn: sqlite3.Connection, scope: Scope, key: str) -> None:
    _layout_check(scope, key)
    conn.execute("DELETE FROM user_layout WHERE staff_id = ? AND dashboard = ?", (scope.staff_id, key))
    conn.commit()
