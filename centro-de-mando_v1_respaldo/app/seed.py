"""Import the Excel maestro (Resources/Excel_Maestro_Importable_Centro_de_Test_MVP_v1_0.xlsx) and
generate FICTITIOUS operational data (invitations, responses, emails) so the Centro de mando can be
validated before the pilot. No real personal data is created (section 15: "usar solo datos ficticios").

Run:  python -m app.seed [--excel PATH] [--db PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import secrets
import sqlite3
from datetime import datetime, timedelta

import openpyxl

from . import db
from .scoring import compute_result

DEFAULT_EXCEL = os.path.join(
    os.path.dirname(__file__), "..", "..", "Resources", "Excel_Maestro_Importable_Centro_de_Test_MVP_v1_0.xlsx"
)

HEADER_KEYS = {
    "USUARIOS": "user_code",
    "TESTS": "test_code",
    "FICHAS_TECNICAS": "test_code",
    "INDICADORES": "indicator_code",
    "ITEMS": "item_code",
    "OPCIONES_RESPUESTA": "scale_code",
    "REGLAS_PUNTUACION": "rule_code",
    "INTERPRETACIONES": "interpretation_code",
    "INVITACIONES_DEMO": "invitation_code",
}


def read_sheet(wb, name: str) -> list[dict]:
    """Return the data rows below the header row (identified by its key column) as dicts."""
    ws = wb[name]
    key = HEADER_KEYS[name]
    header = None
    out = []
    for row in ws.iter_rows(values_only=True):
        if header is None:
            if row and row[0] == key:
                header = [str(h).strip() if h is not None else None for h in row]
            continue
        if not any(v is not None and str(v).strip() for v in row):
            continue
        out.append({h: v for h, v in zip(header, row) if h})
    return out


def _bool(v) -> int:
    if isinstance(v, bool):
        return int(v)
    return int(str(v).strip().lower() in ("true", "1", "sí", "si", "yes", "verdadero"))


def _str(v) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _version(v) -> str:
    s = _str(v) or "1.0"
    return s.replace(",", ".")


def token_hash() -> str:
    # Only the hash of a high-entropy token is stored (section 4.2).
    return hashlib.sha256(secrets.token_urlsafe(32).encode()).hexdigest()


def import_master(conn: sqlite3.Connection, excel_path: str) -> list[str]:
    """Upsert catalogue sheets following MAPA_IMPORTACION order. Returns import warnings."""
    warnings: list[str] = []
    wb = openpyxl.load_workbook(excel_path, data_only=True)

    # 1 USUARIOS -> Company + Person
    for r in read_sheet(wb, "USUARIOS"):
        company = _str(r.get("company_name"))
        email = _str(r.get("email"))
        if not company or not email or "@" not in email:
            warnings.append(f"USUARIOS {r.get('user_code')}: empresa o correo inválido; fila omitida.")
            continue
        conn.execute("INSERT OR IGNORE INTO company(name) VALUES (?)", (company,))
        cid = conn.execute("SELECT id FROM company WHERE name = ?", (company,)).fetchone()["id"]
        created = r.get("created_at")
        conn.execute(
            """INSERT INTO person(user_code, company_id, first_name, last_name, position, dimension, email,
                                  language, status, consent_status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(user_code) DO UPDATE SET company_id=excluded.company_id, first_name=excluded.first_name,
                 last_name=excluded.last_name, position=excluded.position, dimension=excluded.dimension,
                 email=excluded.email, status=excluded.status, consent_status=excluded.consent_status""",
            (r["user_code"], cid, _str(r.get("first_name")), _str(r.get("last_name")), _str(r.get("position")),
             _str(r.get("dimension")), email.lower(), _str(r.get("language")) or "es",
             _str(r.get("status")) or "active", _str(r.get("consent_status")),
             created.isoformat() if isinstance(created, datetime) else _str(created)),
        )

    # 2 TESTS -> TestDefinition
    known_tests = set()
    for r in read_sheet(wb, "TESTS"):
        code = _str(r.get("test_code"))
        if not code:
            warnings.append(f"TESTS '{_str(r.get('test_name'))}': sin test_code; no se importa hasta completarlo.")
            continue
        known_tests.add(code)
        conn.execute(
            """INSERT OR REPLACE INTO test_definition(test_code, name, version, status, purpose, scale_code,
                   expiry_days, reminder_days, ai_report_enabled, license_status)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (code, _str(r.get("test_name")), _version(r.get("version")), _str(r.get("status")),
             _str(r.get("purpose")), _str(r.get("default_scale_code")), int(r.get("expiry_days") or 30),
             int(r.get("reminder_days") or 3), _bool(r.get("ai_report_enabled")), _str(r.get("license_status"))),
        )

    # 3 FICHAS_TECNICAS: tests referenced by a ficha but missing from TESTS are registered as demo tests.
    for r in read_sheet(wb, "FICHAS_TECNICAS"):
        code = _str(r.get("test_code"))
        if code and code not in known_tests:
            if code.endswith("-REF"):
                warnings.append(f"FICHAS_TECNICAS {code}: instrumento de terceros de referencia; no se activa sin licencia.")
                continue
            warnings.append(f"FICHAS_TECNICAS {code}: no figura en TESTS; se registra como test demo v1.0.")
            conn.execute(
                "INSERT OR IGNORE INTO test_definition(test_code, name, version, status, purpose) VALUES (?,?,?,?,?)",
                (code, _str(r.get("name")), "1.0", "demo", "Pruebas técnicas de la plataforma"),
            )
            known_tests.add(code)

    # 4 INDICADORES
    for r in read_sheet(wb, "INDICADORES"):
        conn.execute(
            "INSERT OR REPLACE INTO test_indicator VALUES (?,?,?,?,?,?,?,?,?)",
            (r["test_code"], r["indicator_code"], _str(r.get("indicator_name")), _str(r.get("description")),
             int(r.get("display_order") or 0), float(r.get("weight") or 1), float(r.get("min_score") or 1),
             float(r.get("max_score") or 5), _bool(r.get("active"))),
        )

    # 5 ITEMS
    for r in read_sheet(wb, "ITEMS"):
        if _str(r.get("test_code")) not in known_tests:
            continue
        conn.execute(
            "INSERT OR REPLACE INTO test_item VALUES (?,?,?,?,?,?,?,?,?)",
            (_str(r["item_code"]), r["test_code"], _str(r.get("indicator_code")), _str(r.get("item_text")) or "",
             _str(r.get("response_scale_code")), int(r.get("display_order") or 0),
             _bool(r.get("required")) if r.get("required") is not None else 1,
             _bool(r.get("reverse_scored")) if r.get("reverse_scored") is not None else 0,
             _bool(r.get("active")) if r.get("active") is not None else 1),
        )

    # 6 OPCIONES_RESPUESTA
    for r in read_sheet(wb, "OPCIONES_RESPUESTA"):
        if r.get("value") is None:
            continue
        conn.execute("INSERT OR REPLACE INTO response_option VALUES (?,?,?)",
                     (r["scale_code"], int(r["value"]), _str(r.get("label"))))

    # 7 REGLAS_PUNTUACION
    for r in read_sheet(wb, "REGLAS_PUNTUACION"):
        conn.execute(
            "INSERT OR REPLACE INTO scoring_rule VALUES (?,?,?,?,?,?,?,?,?)",
            (r["rule_code"], r["test_code"], r["level"], _str(r.get("target_code")), _str(r.get("formula_type")),
             float(r.get("weight") or 1), int(r.get("round_decimals") or 0), _version(r.get("scoring_version")),
             _bool(r.get("active"))),
        )

    # 8 INTERPRETACIONES (validated: no overlaps)
    for r in read_sheet(wb, "INTERPRETACIONES"):
        conn.execute(
            "INSERT OR REPLACE INTO interpretation_rule VALUES (?,?,?,?,?,?,?,?,?)",
            (r["interpretation_code"], r["test_code"], r["target_code"], float(r["min_score"]),
             float(r["max_score"]), r["level_name"], _str(r.get("approved_text")),
             _str(r.get("recommended_action")), _bool(r.get("active"))),
        )
    for t in known_tests:
        rows = conn.execute("SELECT * FROM interpretation_rule WHERE test_code = ? ORDER BY min_score", (t,)).fetchall()
        for a, b in zip(rows, rows[1:]):
            if b["min_score"] <= a["max_score"]:
                warnings.append(f"INTERPRETACIONES {t}: rangos solapados {a['interpretation_code']}/{b['interpretation_code']}.")

    # Tests without approved indicators cannot produce indicator results.
    for t in sorted(known_tests):
        if not conn.execute("SELECT 1 FROM test_indicator WHERE test_code = ?", (t,)).fetchone():
            warnings.append(f"{t}: sin indicadores ni reglas de puntuación en el Excel; solo métricas operativas.")

    # INVITACIONES_DEMO references user codes that do not exist in USUARIOS.
    for r in read_sheet(wb, "INVITACIONES_DEMO"):
        if not conn.execute("SELECT 1 FROM person WHERE user_code = ?", (r.get("user_code"),)).fetchone():
            warnings.append(f"INVITACIONES_DEMO {r['invitation_code']}: user_code {r.get('user_code')} no existe en USUARIOS; omitida.")

    conn.commit()
    return warnings


# ---------------------------------------------------------------------------------------------
# Fictitious operational data
# ---------------------------------------------------------------------------------------------
FIRST = ["Lucía", "Hugo", "Sofía", "Martín", "Paula", "Diego", "Alba", "Javier", "Irene", "Álvaro", "Clara",
         "Sergio", "Noelia", "Raúl", "Carmen", "Andrés", "Julia", "Víctor", "Sara", "Iván", "Rocío", "Adrián",
         "Beatriz", "Gonzalo", "Marta", "Rubén", "Eva", "Óscar", "Inés", "Manuel", "Lorena", "Tomás"]
LAST = ["Navarro", "Romero", "Molina", "Ortega", "Delgado", "Castro", "Ortiz", "Rubio", "Marín", "Sanz",
        "Iglesias", "Núñez", "Medina", "Garrido", "Cortés", "Lozano", "Gil", "Prieto", "Vidal", "Cano"]
POSITIONS = [("Participante", "Persona"), ("Participante", "Persona"), ("Participante", "Persona"),
             ("Líder de equipo", "Equipo"), ("Responsable de RRHH", "Organizativa")]
STAFF = [
    ("admin@agileinstitute.es", "Administración Agile Institute", "admin"),
    ("gestor@agileinstitute.es", "Gestor de test", "gestor"),
    ("consultor@agileinstitute.es", "Consultor asignado (Empresa Demo A)", "consultor"),
    ("visor@agileinstitute.es", "Visor (Empresa Demo B · demo)", "visor"),
]


def _iso(d: datetime | None) -> str | None:
    return d.isoformat(timespec="seconds") if d else None


def generate_demo(conn: sqlite3.Connection, today: datetime | None = None, seed: int = 42) -> dict:
    rnd = random.Random(seed)
    today = (today or datetime.now()).replace(microsecond=0)

    conn.execute("INSERT OR IGNORE INTO company(name) VALUES ('Empresa Demo C')")
    companies = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM company")}

    # Extra fictitious people so aggregated indicators reach the minimum sample.
    sizes = {"Empresa Demo A": 18, "Empresa Demo B": 14, "Empresa Demo C": 10}
    n = 0
    for cname, target in sizes.items():
        have = conn.execute("SELECT COUNT(*) c FROM person WHERE company_id = ?", (companies[cname],)).fetchone()["c"]
        for _ in range(max(0, target - have)):
            n += 1
            fn, ln = rnd.choice(FIRST), rnd.choice(LAST)
            pos, dim = rnd.choice(POSITIONS)
            email = f"{fn}.{ln}.{n}@example.com".lower()
            for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")):
                email = email.replace(a, b)
            conn.execute(
                """INSERT INTO person(user_code, company_id, first_name, last_name, position, dimension, email,
                       status, consent_status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (f"USR-D{n:03d}", companies[cname], fn, ln, pos, dim, email, "active", "accepted",
                 _iso(today - timedelta(days=200))),
            )

    tests = {r["test_code"]: r for r in conn.execute("SELECT * FROM test_definition")}
    scored = [t for t in tests if conn.execute("SELECT 1 FROM scoring_rule WHERE test_code = ?", (t,)).fetchone()]
    unscored = [t for t in tests if t not in scored]
    items = {t: conn.execute("SELECT * FROM test_item WHERE test_code = ? AND active = 1", (t,)).fetchall()
             for t in scored}
    people = conn.execute("SELECT p.*, c.name company FROM person p JOIN company c ON c.id = p.company_id").fetchall()
    # Company-level tendency so comparisons by company are visible.
    company_bias = {"Empresa Demo A": 0.35, "Empresa Demo B": -0.15, "Empresa Demo C": 0.05}

    inv_n = 0
    stats = {"invitations": 0, "completed": 0, "reminders": 0}

    def new_invitation(person, test_code, sent_at):
        nonlocal inv_n
        inv_n += 1
        t = tests[test_code]
        expires = sent_at + timedelta(days=t["expiry_days"] or 30)
        cur = conn.execute(
            """INSERT INTO invitation(invitation_code, person_id, test_code, test_version, token_hash, sent_at,
                   expires_at, report_allowed) VALUES (?,?,?,?,?,?,?,?)""",
            (f"INV-{inv_n:04d}", person["id"], test_code, t["version"], token_hash(), _iso(sent_at), _iso(expires),
             1 if rnd.random() < 0.85 else 0),
        )
        conn.execute("INSERT INTO email_log(type, invitation_id, recipient, result, provider, sent_at) VALUES (?,?,?,?,?,?)",
                     ("invitation", cur.lastrowid, person["email"], "delivered", "resend", _iso(sent_at)))
        stats["invitations"] += 1
        return cur.lastrowid, expires

    # Scored tests: monthly waves over the last ~7 months, some people measured twice (before/after).
    for test_code in scored:
        traits = {}
        for p in people:
            waves = rnd.choice([1, 1, 2]) if p["status"] == "active" else 1
            start_offsets = sorted(rnd.sample(range(5, 210), waves), reverse=True)
            for wave, days_ago in enumerate(start_offsets):
                sent = (today - timedelta(days=days_ago)).replace(hour=rnd.randint(8, 18), minute=rnd.choice([0, 15, 30, 45]), second=0)
                inv_id, expires = new_invitation(p, test_code, sent)
                elapsed = (today - sent).days
                behaviour = rnd.random()
                completed = None
                if behaviour < 0.72:  # completes
                    delay = timedelta(hours=rnd.choice([2, 5, 20, 30, 50, 70, 100, 150, 240, 400]) + rnd.random() * 10)
                    if sent + delay <= min(today, expires):
                        completed = sent + delay
                reminder = None
                due = sent + timedelta(days=tests[test_code]["reminder_days"] or 3)
                if due <= today and (completed is None or completed > due):
                    reminder = due.replace(hour=9, minute=0)
                    conn.execute("UPDATE invitation SET reminder_sent_at = ? WHERE id = ?", (_iso(reminder), inv_id))
                    conn.execute("INSERT INTO email_log(type, invitation_id, recipient, result, provider, sent_at) VALUES (?,?,?,?,?,?)",
                                 ("reminder", inv_id, p["email"], "delivered", "resend", _iso(reminder)))
                    stats["reminders"] += 1
                if completed:
                    key = p["id"]
                    if key not in traits:
                        base = 3.2 + company_bias.get(p["company"], 0)
                        traits[key] = {ind: base + rnd.gauss(0, 0.55) + off for ind, off in
                                       {"ADA": 0.1, "COL": 0.45, "VAL": -0.2, "APR": 0.15, "IA": -0.35}.items()}
                    growth = 0.25 * wave  # second measurement slightly higher
                    for it in items[test_code]:
                        mu = traits[key].get(it["indicator_code"], 3.2) + growth
                        v = max(1, min(5, round(rnd.gauss(mu, 0.7))))
                        if it["reverse_scored"]:
                            v = 6 - v
                        conn.execute("INSERT INTO response VALUES (?,?,?,?)", (inv_id, it["item_code"], v, _iso(completed)))
                    conn.execute("UPDATE invitation SET completed_at = ?, report_status = ? WHERE id = ?",
                                 (_iso(completed), "sent", inv_id))
                    compute_result(conn, inv_id, now=completed)
                    conn.execute("INSERT INTO email_log(type, invitation_id, recipient, result, provider, sent_at) VALUES (?,?,?,?,?,?)",
                                 ("completed", inv_id, p["email"], "delivered", "resend", _iso(completed)))
                    stats["completed"] += 1

    # Current wave for scored tests: recent sends, about half still pending (exercise pending/reminder states).
    for test_code in scored:
        for p in rnd.sample(list(people), k=min(12, len(people))):
            sent = (today - timedelta(days=rnd.randint(1, 20))).replace(hour=9, minute=30, second=0)
            inv_id, _ = new_invitation(p, test_code, sent)
            due = sent + timedelta(days=tests[test_code]["reminder_days"] or 3)
            if rnd.random() < 0.5 and due <= today:
                completed = min(today, sent + timedelta(hours=rnd.choice([3, 26, 48])))
                for it in items[test_code]:
                    v = max(1, min(5, round(rnd.gauss(3.4, 0.8))))
                    conn.execute("INSERT INTO response VALUES (?,?,?,?)", (inv_id, it["item_code"], v, _iso(completed)))
                conn.execute("UPDATE invitation SET completed_at = ?, report_status = 'sent' WHERE id = ?",
                             (_iso(completed), inv_id))
                compute_result(conn, inv_id, now=completed)
                stats["completed"] += 1
            elif due <= today:
                conn.execute("UPDATE invitation SET reminder_sent_at = ? WHERE id = ?", (_iso(due), inv_id))
                conn.execute("INSERT INTO email_log(type, invitation_id, recipient, result, provider, sent_at) VALUES (?,?,?,?,?,?)",
                             ("reminder", inv_id, p["email"], "delivered", "resend", _iso(due)))
                stats["reminders"] += 1

    # Unscored pilot tests (e.g. DEMO-AGILE-50): recent sends, operational metrics only.
    for test_code in unscored:
        for p in rnd.sample(list(people), k=min(9, len(people))):
            sent = (today - timedelta(days=rnd.randint(1, 9))).replace(hour=10, minute=0, second=0)
            inv_id, _ = new_invitation(p, test_code, sent)
            due = sent + timedelta(days=3)
            if due <= today:
                conn.execute("UPDATE invitation SET reminder_sent_at = ? WHERE id = ?", (_iso(due), inv_id))
                conn.execute("INSERT INTO email_log(type, invitation_id, recipient, result, provider, sent_at) VALUES (?,?,?,?,?,?)",
                             ("reminder", inv_id, p["email"], "delivered", "resend", _iso(due)))
                stats["reminders"] += 1

    # Staff accounts and their scopes (section 3, roles y permisos).
    for email, name, role in STAFF:
        conn.execute("INSERT OR IGNORE INTO staff_user(email, name, role) VALUES (?,?,?)", (email, name, role))
    staff = {r["role"]: r["id"] for r in conn.execute("SELECT id, role FROM staff_user")}
    conn.execute("INSERT OR IGNORE INTO staff_company_access VALUES (?,?)", (staff["consultor"], companies["Empresa Demo A"]))
    if scored:
        conn.execute("INSERT OR IGNORE INTO dashboard_share VALUES (?,?,?)",
                     (staff["visor"], companies["Empresa Demo B"], scored[0]))
    conn.commit()
    return stats


def build_database(db_path: str | None = None, excel_path: str | None = None, today: datetime | None = None,
                   reset: bool = True) -> tuple[sqlite3.Connection, list[str], dict]:
    db_path = db_path or os.environ.get("CDM_DB_PATH", db.DEFAULT_DB_PATH)
    if reset and db_path != ":memory:" and os.path.exists(db_path):
        os.remove(db_path)
    conn = db.connect(db_path)
    db.init_schema(conn)
    warnings = import_master(conn, excel_path or os.environ.get("CDM_EXCEL_PATH", DEFAULT_EXCEL))
    stats = generate_demo(conn, today=today)
    return conn, warnings, stats


def main() -> None:
    ap = argparse.ArgumentParser(description="Importa el Excel maestro y genera datos ficticios.")
    ap.add_argument("--excel", default=None)
    ap.add_argument("--db", default=None)
    args = ap.parse_args()
    conn, warnings, stats = build_database(args.db, args.excel)
    print("Importación completada:", stats)
    for w in warnings:
        print("  aviso:", w)
    conn.close()


if __name__ == "__main__":
    main()
