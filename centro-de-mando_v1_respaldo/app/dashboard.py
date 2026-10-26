"""Centro de mando: aggregated analytics (section 7 of the functional document).

Every query goes through `Scope`, so permissions are enforced in the backend, never only in the UI
(section 15: "Aplicar permisos en backend, no solo ocultar botones").
"""
from __future__ import annotations

import os
import sqlite3
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime

from .scoring import round_half_up

MIN_SAMPLE = int(os.environ.get("CDM_MIN_SAMPLE", "3"))

STATUS_LABELS = {"completed": "Realizado", "pending": "Pendiente", "expired": "Caducado"}


class Forbidden(Exception):
    pass


@dataclass
class Scope:
    staff_id: int
    email: str
    name: str
    role: str
    company_ids: set[int] | None = None          # None = all companies
    shares: set[tuple[int, str]] = field(default_factory=set)  # visor: (company_id, test_code)

    @property
    def can_see_individuals(self) -> bool:
        return self.role in ("admin", "consultor")

    @property
    def can_export_items(self) -> bool:
        return self.role == "admin"


def scope_for(conn: sqlite3.Connection, staff_id: int) -> Scope:
    s = conn.execute("SELECT * FROM staff_user WHERE id = ?", (staff_id,)).fetchone()
    if s is None:
        raise Forbidden("Usuario no encontrado.")
    if s["role"] == "gestor":
        # Section 3: the gestor de test manages users, sends, reports and states, not dashboards.
        raise Forbidden("El rol Gestor de test no tiene acceso a los cuadros de mando.")
    scope = Scope(staff_id=s["id"], email=s["email"], name=s["name"], role=s["role"])
    if s["role"] == "consultor":
        scope.company_ids = {r["company_id"] for r in conn.execute(
            "SELECT company_id FROM staff_company_access WHERE staff_id = ?", (staff_id,))}
    elif s["role"] == "visor":
        scope.shares = {(r["company_id"], r["test_code"]) for r in conn.execute(
            "SELECT company_id, test_code FROM dashboard_share WHERE staff_id = ?", (staff_id,))}
        scope.company_ids = {c for c, _ in scope.shares}
    return scope


@dataclass
class Filters:
    company_id: int | None = None
    test_code: str | None = None
    date_from: str | None = None   # YYYY-MM-DD, applied to sent_at
    date_to: str | None = None

    def describe(self, conn: sqlite3.Connection) -> dict:
        company = None
        if self.company_id:
            row = conn.execute("SELECT name FROM company WHERE id = ?", (self.company_id,)).fetchone()
            company = row["name"] if row else None
        test = None
        if self.test_code:
            row = conn.execute("SELECT name, version FROM test_definition WHERE test_code = ?", (self.test_code,)).fetchone()
            test = f"{row['name']} (v{row['version']})" if row else self.test_code
        return {"Empresa": company or "Todas las autorizadas", "Test": test or "Todos los autorizados",
                "Desde": self.date_from or "Inicio", "Hasta": self.date_to or "Hoy"}


def invitation_status(inv, now: datetime) -> str:
    """Section 4.4: realizado if completed_at; caducado if now > expires_at; else pendiente."""
    if inv["completed_at"]:
        return "completed"
    if now > datetime.fromisoformat(inv["expires_at"]):
        return "expired"
    return "pending"


def _where(scope: Scope, f: Filters, alias: str = "i") -> tuple[str, list]:
    clauses, params = [], []
    if scope.company_ids is not None:
        if not scope.company_ids:
            return "1 = 0", []
        clauses.append(f"p.company_id IN ({','.join('?' * len(scope.company_ids))})")
        params += sorted(scope.company_ids)
    if scope.role == "visor":
        pairs = sorted(scope.shares)
        if not pairs:
            return "1 = 0", []
        clauses.append("(" + " OR ".join(f"(p.company_id = ? AND {alias}.test_code = ?)" for _ in pairs) + ")")
        for c, t in pairs:
            params += [c, t]
    if f.company_id:
        clauses.append("p.company_id = ?")
        params.append(f.company_id)
    if f.test_code:
        clauses.append(f"{alias}.test_code = ?")
        params.append(f.test_code)
    if f.date_from:
        clauses.append(f"{alias}.sent_at >= ?")
        params.append(f.date_from)
    if f.date_to:
        clauses.append(f"{alias}.sent_at < date(?, '+1 day')")
        params.append(f.date_to)
    return (" AND ".join(clauses) or "1 = 1"), params


def scoped_invitations(conn: sqlite3.Connection, scope: Scope, f: Filters) -> list[sqlite3.Row]:
    where, params = _where(scope, f)
    return conn.execute(
        f"""SELECT i.*, p.first_name, p.last_name, p.position, p.email, p.company_id, c.name AS company,
                   t.name AS test_name
            FROM invitation i
            JOIN person p ON p.id = i.person_id
            JOIN company c ON c.id = p.company_id
            JOIN test_definition t ON t.test_code = i.test_code
            WHERE {where}
            ORDER BY i.sent_at DESC""",
        params,
    ).fetchall()


def filter_options(conn: sqlite3.Connection, scope: Scope) -> dict:
    where, params = _where(scope, Filters())
    companies = conn.execute(
        f"""SELECT DISTINCT c.id, c.name FROM company c JOIN person p ON p.company_id = c.id
            LEFT JOIN invitation i ON i.person_id = p.id WHERE {where} ORDER BY c.name""", params).fetchall()
    tests = conn.execute(
        f"""SELECT DISTINCT t.test_code, t.name, t.version, t.status,
                   EXISTS (SELECT 1 FROM test_indicator ti WHERE ti.test_code = t.test_code) AS has_indicators
            FROM test_definition t JOIN invitation i ON i.test_code = t.test_code
            JOIN person p ON p.id = i.person_id WHERE {where} ORDER BY has_indicators DESC, t.name""",
        params).fetchall()
    return {
        "companies": [dict(r) for r in companies],
        "tests": [dict(r) | {"has_indicators": bool(r["has_indicators"])} for r in tests],
        "min_sample": MIN_SAMPLE,
    }


def _month(iso: str) -> str:
    return iso[:7]


def _levels(conn: sqlite3.Connection, test_code: str) -> list[dict]:
    rows = conn.execute(
        """SELECT level_name, MIN(min_score) lo, MAX(max_score) hi FROM interpretation_rule
           WHERE test_code = ? AND active = 1 GROUP BY level_name ORDER BY lo""", (test_code,)).fetchall()
    return [{"name": r["level_name"], "min": r["lo"], "max": r["hi"]} for r in rows]


def _indicators(conn: sqlite3.Connection, test_code: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM test_indicator WHERE test_code = ? AND active = 1 ORDER BY display_order", (test_code,)).fetchall()


def results_for(conn: sqlite3.Connection, invitation_ids: list[int]) -> dict[int, dict[str, sqlite3.Row]]:
    out: dict[int, dict[str, sqlite3.Row]] = defaultdict(dict)
    for chunk_start in range(0, len(invitation_ids), 500):
        chunk = invitation_ids[chunk_start:chunk_start + 500]
        if not chunk:
            continue
        for r in conn.execute(
                f"SELECT * FROM result WHERE invitation_id IN ({','.join('?' * len(chunk))})", chunk):
            out[r["invitation_id"]][r["target_code"]] = r
    return out


def dashboard(conn: sqlite3.Connection, scope: Scope, f: Filters, now: datetime | None = None) -> dict:
    now = now or datetime.now()
    invs = scoped_invitations(conn, scope, f)
    statuses = [invitation_status(i, now) for i in invs]
    counts = Counter(statuses)
    sent = len(invs)

    # 4. Tiempo medio de respuesta: sent_at -> completed_at
    durations = [(datetime.fromisoformat(i["completed_at"]) - datetime.fromisoformat(i["sent_at"])).total_seconds() / 86400
                 for i in invs if i["completed_at"]]

    # 5. Recordatorios enviados (by reminder date within the period, for the scoped company/test).
    where, params = _where(scope, Filters(company_id=f.company_id, test_code=f.test_code))
    rq = f"""SELECT COUNT(*) n FROM email_log e JOIN invitation i ON i.id = e.invitation_id
             JOIN person p ON p.id = i.person_id WHERE e.type = 'reminder' AND {where}"""
    if f.date_from:
        rq += " AND e.sent_at >= ?"
        params.append(f.date_from)
    if f.date_to:
        rq += " AND e.sent_at < date(?, '+1 day')"
        params.append(f.date_to)
    reminders = conn.execute(rq, params).fetchone()["n"]

    by_company: dict[str, Counter] = defaultdict(Counter)
    for i, s in zip(invs, statuses):
        by_company[i["company"]][s] += 1

    kpis = {
        "sent": sent,
        "completed": counts["completed"],
        "pending": counts["pending"],
        "expired": counts["expired"],
        "completion_rate": round(counts["completed"] / sent, 4) if sent else None,
        "avg_response_days": round(statistics.mean(durations), 1) if durations else None,
        "median_response_days": round(statistics.median(durations), 1) if durations else None,
        "reminders": reminders,
    }

    # Monthly operational evolution (always comparable: counts).
    sent_month = Counter(_month(i["sent_at"]) for i in invs)
    done_month = Counter(_month(i["completed_at"]) for i in invs if i["completed_at"])
    months = sorted(set(sent_month) | set(done_month))
    activity = [{"period": m, "sent": sent_month.get(m, 0), "completed": done_month.get(m, 0)} for m in months]

    out = {
        "generated_at": now.isoformat(timespec="seconds"),
        "filters": f.describe(conn),
        "scope": {"role": scope.role, "name": scope.name, "can_see_individuals": scope.can_see_individuals,
                  "can_export_items": scope.can_export_items, "min_sample": MIN_SAMPLE},
        "kpis": kpis,
        "status_by_company": [
            {"company": c, "completed": v["completed"], "pending": v["pending"], "expired": v["expired"],
             "sent": sum(v.values())} for c, v in sorted(by_company.items())],
        "activity": activity,
        "results": _results_section(conn, f, invs),
    }
    return out


def _results_section(conn: sqlite3.Connection, f: Filters, invs: list[sqlite3.Row]) -> dict:
    """6-8: indicator means, level distribution and temporal evolution (one test at a time)."""
    if not f.test_code:
        return {"available": False, "reason": "Selecciona un test para ver resultados por indicador."}
    indicators = _indicators(conn, f.test_code)
    if not indicators:
        return {"available": False,
                "reason": "Este test no tiene indicadores ni reglas de puntuación aprobadas; solo se muestran métricas operativas."}

    done = [i for i in invs if i["completed_at"]]
    res = results_for(conn, [i["id"] for i in done])
    # Comparable measurements = same test_version + scoring_version; keep the latest version family.
    versions = Counter((r["test_version"], r["scoring_version"]) for rr in res.values() for r in rr.values()
                       if r["target_code"] == "GLOBAL")
    if not versions:
        return {"available": False, "reason": "Aún no hay resultados calculados para los filtros elegidos."}
    test_version, scoring_version = max(versions)
    done = [i for i in done if "GLOBAL" in res.get(i["id"], {})
            and res[i["id"]]["GLOBAL"]["test_version"] == test_version
            and res[i["id"]]["GLOBAL"]["scoring_version"] == scoring_version]
    n = len(done)
    levels = _levels(conn, f.test_code)
    targets = [("GLOBAL", "Resultado global")] + [(i["indicator_code"], i["name"]) for i in indicators]
    lo = min(i["min_score"] for i in indicators)
    hi = max(i["max_score"] for i in indicators)

    base = {"available": True, "n": n, "min_sample": MIN_SAMPLE, "test_version": test_version,
            "scoring_version": scoring_version, "scale": {"min": lo, "max": hi}, "levels": levels,
            "excluded_other_versions": sum(versions.values()) - versions[(test_version, scoring_version)]}
    if n < MIN_SAMPLE:
        return base | {"suppressed": True,
                       "reason": f"Muestra insuficiente: {n} resultados (mínimo {MIN_SAMPLE}) para mostrar agregados."}

    means, distribution = [], []
    for code, name in targets:
        scores = [res[i["id"]][code]["score"] for i in done if code in res[i["id"]] and res[i["id"]][code]["score"] is not None]
        lv = Counter(res[i["id"]][code]["level_name"] for i in done if code in res[i["id"]])
        mean = round_half_up(statistics.mean(scores), 2) if scores else None
        level = None
        if mean is not None:
            level = next((l["name"] for l in levels if l["min"] <= mean <= l["max"]), None)
        means.append({"code": code, "name": name, "mean": mean, "n": len(scores), "level": level,
                      "min": min(scores) if scores else None, "max": max(scores) if scores else None,
                      "sd": round(statistics.stdev(scores), 2) if len(scores) > 1 else None})
        distribution.append({"code": code, "name": name,
                             "counts": [{"level": l["name"], "count": lv.get(l["name"], 0)} for l in levels],
                             "total": len(scores)})

    # Evolution: monthly mean of the global result, only periods meeting the minimum sample.
    by_month: dict[str, list[float]] = defaultdict(list)
    for i in done:
        s = res[i["id"]]["GLOBAL"]["score"]
        if s is not None:
            by_month[_month(i["completed_at"])].append(s)
    series = [{"period": m, "n": len(v), "mean": round_half_up(statistics.mean(v), 2) if len(v) >= MIN_SAMPLE else None,
               "suppressed": len(v) < MIN_SAMPLE} for m, v in sorted(by_month.items())]
    comparable_points = [p for p in series if not p["suppressed"]]
    evolution = {"available": len(comparable_points) > 1, "series": series,
                 "reason": None if len(comparable_points) > 1 else
                 "Se necesita más de una medición comparable (mismo test y versión) con muestra suficiente."}
    return base | {"suppressed": False, "means": means, "distribution": distribution, "evolution": evolution}


def result_rows(conn: sqlite3.Connection, scope: Scope, f: Filters, now: datetime | None = None) -> dict:
    """Filterable individual result table (Excel 'Resultados'). Not available to the visor role."""
    if not scope.can_see_individuals:
        raise Forbidden("Tu rol solo permite consultar indicadores agregados.")
    now = now or datetime.now()
    invs = scoped_invitations(conn, scope, f)
    res = results_for(conn, [i["id"] for i in invs if i["completed_at"]])
    indicators = _indicators(conn, f.test_code) if f.test_code else []
    rows = []
    for i in invs:
        st = invitation_status(i, now)
        r = res.get(i["id"], {})
        days = None
        if i["completed_at"]:
            days = round((datetime.fromisoformat(i["completed_at"]) - datetime.fromisoformat(i["sent_at"])).total_seconds() / 86400, 1)
        g = r.get("GLOBAL")
        rows.append({
            "invitation_code": i["invitation_code"], "company": i["company"],
            "person": f"{i['first_name']} {i['last_name']}", "position": i["position"],
            "test_code": i["test_code"], "test_name": i["test_name"], "test_version": i["test_version"],
            "status": st, "status_label": STATUS_LABELS[st],
            "sent_at": i["sent_at"], "expires_at": i["expires_at"], "completed_at": i["completed_at"],
            "response_days": days, "reminder_sent_at": i["reminder_sent_at"],
            "global": g["score"] if g else None, "level": g["level_name"] if g else None,
            "scoring_version": g["scoring_version"] if g else None,
            "scores": {ind["indicator_code"]: (r[ind["indicator_code"]]["score"] if ind["indicator_code"] in r else None)
                       for ind in indicators},
        })
    return {"indicators": [{"code": i["indicator_code"], "name": i["name"]} for i in indicators], "rows": rows}


def item_responses(conn: sqlite3.Connection, scope: Scope, f: Filters) -> list[dict]:
    """Item-level answers: only for an expressly authorised administrative export."""
    if not scope.can_export_items:
        raise Forbidden("La exportación de respuestas ítem a ítem solo está autorizada a administración.")
    where, params = _where(scope, f)
    rows = conn.execute(
        f"""SELECT i.invitation_code, c.name company, p.first_name || ' ' || p.last_name person, i.test_code,
                   i.test_version, r.item_code, ti.indicator_code, ti.item_text, ti.reverse_scored, r.value, r.answered_at
            FROM response r JOIN invitation i ON i.id = r.invitation_id
            JOIN person p ON p.id = i.person_id JOIN company c ON c.id = p.company_id
            LEFT JOIN test_item ti ON ti.test_code = i.test_code AND ti.item_code = r.item_code
            WHERE {where} ORDER BY i.invitation_code, ti.display_order""", params).fetchall()
    return [dict(r) for r in rows]
