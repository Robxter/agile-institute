import io
import os
from datetime import datetime

import openpyxl
import pytest
from fastapi.testclient import TestClient

from app import main
from app.dashboard import Filters, dashboard, invitation_status, scope_for
from app.scoring import compute_result, interpret, round_half_up
from app.seed import build_database

TODAY = datetime(2026, 10, 16, 12, 0)


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("db") / "test.db")
    c, warnings, stats = build_database(path, today=TODAY)
    assert stats["completed"] > 0
    yield c
    c.close()


@pytest.fixture()
def client(conn):
    main.set_connection(conn)
    return TestClient(main.app)


def login(client, role):
    r = client.post("/api/auth/login", json={"email": f"{role}@agileinstitute.es"})
    assert r.status_code == 200


def staff_id(conn, role):
    return conn.execute("SELECT id FROM staff_user WHERE role = ?", (role,)).fetchone()["id"]


# ------------------------------------------------------------------ scoring (PA-05)
def test_scoring_matches_manual_calculation(conn):
    inv = conn.execute("SELECT id FROM invitation WHERE test_code = 'DEMO-AGILE-12' AND completed_at IS NOT NULL LIMIT 1").fetchone()["id"]
    answers = {f"DEM-{n:03d}": v for n, v in zip(range(1, 13), [4, 2, 5, 4, 3, 1, 4, 5, 3, 4, 5, 2])}
    conn.execute("DELETE FROM response WHERE invitation_id = ?", (inv,))
    for code, v in answers.items():
        conn.execute("INSERT INTO response VALUES (?,?,?,?)", (inv, code, v, "2026-09-01T10:00:00"))
    out = compute_result(conn, inv)
    # Manual (Excel) check: DEM-002 and DEM-006 are reversed as 6 - x.
    ada = (4 + (6 - 2)) / 2                # 4.00
    col = (5 + 4 + 5) / 3                  # 4.67
    val = (3 + (6 - 1) + 2) / 3            # 3.33
    apr = (4 + 5) / 2                      # 4.50
    ia = (3 + 4) / 2                       # 3.50
    assert out["indicators"] == {"ADA": 4.0, "COL": 4.67, "VAL": 3.33, "APR": 4.5, "IA": 3.5}
    assert out["global"] == round_half_up((4.0 + 4.67 + 3.33 + 4.5 + 3.5) / 5, 2) == 4.0
    level = conn.execute("SELECT level_name FROM result WHERE invitation_id = ? AND target_code = 'COL'", (inv,)).fetchone()
    assert level["level_name"] == "Referente"
    conn.rollback()


def test_interpretation_boundaries(conn):
    assert interpret(conn, "DEMO-AGILE-12", "ADA", 1.79) == "Inicial"
    assert interpret(conn, "DEMO-AGILE-12", "ADA", 1.80) == "En desarrollo"
    assert interpret(conn, "DEMO-AGILE-12", "GLOBAL", 4.2) == "Referente"
    assert interpret(conn, "DEMO-AGILE-12", "ADA", 5.0) == "Referente"


# ------------------------------------------------------------------ states (4.4)
def test_status_rules():
    base = {"completed_at": None, "expires_at": "2026-10-10T00:00:00"}
    assert invitation_status(base, datetime(2026, 10, 9)) == "pending"
    assert invitation_status(base, datetime(2026, 10, 11)) == "expired"
    assert invitation_status({**base, "completed_at": "2026-10-01T10:00:00"}, datetime(2026, 12, 1)) == "completed"


# ------------------------------------------------------------------ KPIs (section 7)
def test_kpis_are_consistent(conn):
    data = dashboard(conn, scope_for(conn, staff_id(conn, "admin")), Filters(test_code="DEMO-AGILE-12"), now=TODAY)
    k = data["kpis"]
    assert k["sent"] == k["completed"] + k["pending"] + k["expired"]
    assert k["completion_rate"] == round(k["completed"] / k["sent"], 4)
    assert k["avg_response_days"] > 0
    assert k["reminders"] > 0
    r = data["results"]
    assert r["available"] and not r["suppressed"]
    assert r["means"][0]["code"] == "GLOBAL"
    assert sum(c["count"] for c in r["distribution"][0]["counts"]) == r["n"]
    assert r["evolution"]["available"]


def test_period_filter_narrows(conn):
    scope = scope_for(conn, staff_id(conn, "admin"))
    all_ = dashboard(conn, scope, Filters(), now=TODAY)["kpis"]["sent"]
    recent = dashboard(conn, scope, Filters(date_from="2026-09-16", date_to="2026-10-16"), now=TODAY)["kpis"]["sent"]
    assert 0 < recent < all_


def test_unscored_test_shows_only_operational(conn):
    data = dashboard(conn, scope_for(conn, staff_id(conn, "admin")), Filters(test_code="DEMO-AGILE-50"), now=TODAY)
    assert data["kpis"]["sent"] > 0
    assert data["results"]["available"] is False


def test_min_sample_suppresses_aggregates(conn, monkeypatch):
    from app import dashboard as d
    monkeypatch.setattr(d, "MIN_SAMPLE", 10_000)
    data = d.dashboard(conn, scope_for(conn, staff_id(conn, "admin")), Filters(test_code="DEMO-AGILE-12"), now=TODAY)
    assert data["results"]["suppressed"] is True
    assert "means" not in data["results"]


# ------------------------------------------------------------------ roles & permissions (section 3, PA-10)
def test_requires_session(client):
    client.cookies.clear()
    assert client.get("/api/dashboard").status_code == 401


def test_gestor_has_no_dashboard(client):
    login(client, "gestor")
    assert client.get("/api/auth/me").json()["dashboard_access"] is False
    assert client.get("/api/dashboard").status_code == 403


def test_consultor_sees_only_assigned_company(client, conn):
    login(client, "consultor")
    opts = client.get("/api/filters").json()
    assert [c["name"] for c in opts["companies"]] == ["Empresa Demo A"]
    rows = client.get("/api/results").json()["rows"]
    assert rows and {r["company"] for r in rows} == {"Empresa Demo A"}
    other = conn.execute("SELECT id FROM company WHERE name = 'Empresa Demo B'").fetchone()["id"]
    assert client.get(f"/api/dashboard?company_id={other}").status_code == 403
    assert client.get("/api/export.xlsx?include_responses=true&reason=verificacion manual").status_code == 403


def test_visor_only_aggregates_of_shared_dashboard(client):
    login(client, "visor")
    opts = client.get("/api/filters").json()
    assert [c["name"] for c in opts["companies"]] == ["Empresa Demo B"]
    assert [t["test_code"] for t in opts["tests"]] == ["DEMO-AGILE-12"]
    assert client.get("/api/results").status_code == 403
    assert client.get("/api/dashboard?test_code=DEMO-AGILE-50").status_code == 403
    data = client.get("/api/dashboard").json()
    assert {r["company"] for r in data["status_by_company"]} == {"Empresa Demo B"}
    wb = openpyxl.load_workbook(io.BytesIO(client.get("/api/export.xlsx?test_code=DEMO-AGILE-12").content))
    assert "Resultados" not in wb.sheetnames


# ------------------------------------------------------------------ Excel (PA-09) and audit
def test_admin_excel_export(client, conn):
    login(client, "admin")
    r = client.get("/api/export.xlsx?test_code=DEMO-AGILE-12")
    assert r.status_code == 200
    wb = openpyxl.load_workbook(io.BytesIO(r.content))
    assert wb.sheetnames == ["Resumen", "Resultados", "Indicadores", "Trazabilidad"]
    assert len(wb["Resumen"]._charts) >= 4
    res = wb["Resultados"]
    assert "Resultados" in res.tables  # filterable Excel table
    assert res.cell(row=1, column=13).value == "Resultado global"
    last = conn.execute("SELECT action, detail FROM audit_event ORDER BY id DESC LIMIT 1").fetchone()
    assert last["action"] == "dashboard.export_xlsx"


def test_item_level_export_requires_reason(client):
    login(client, "admin")
    assert client.get("/api/export.xlsx?test_code=DEMO-AGILE-12&include_responses=true").status_code == 400
    r = client.get("/api/export.xlsx?test_code=DEMO-AGILE-12&include_responses=true&reason=Verificación manual PA-05")
    assert r.status_code == 200
    wb = openpyxl.load_workbook(io.BytesIO(r.content))
    assert "Respuestas" in wb.sheetnames
    assert wb["Respuestas"].max_row > 12


def test_default_export_excludes_item_answers(client):
    login(client, "admin")
    wb = openpyxl.load_workbook(io.BytesIO(client.get("/api/export.xlsx").content))
    assert "Respuestas" not in wb.sheetnames


def test_frontend_served(client):
    assert "Centro de mando" in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
