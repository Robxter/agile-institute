import io

import openpyxl
import pytest
from fastapi.testclient import TestClient

from app import db, main
from app.catalog import get_catalog
from app.dashboard import (DASHBOARDS, MIN_GROUP, Filters, Forbidden, build, profile, resolve_filters, scope_for)
from app.importer import import_workbook
from app.scoring import block_scores, parse_raw, round_half_up
from app.seed import build_database


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    c, stats = build_database(str(tmp_path_factory.mktemp("db") / "test.db"))
    assert stats["evaluations"] > 0
    yield c
    c.close()


@pytest.fixture()
def client(conn):
    main.set_connection(conn)
    return TestClient(main.app)


def login(client, email):
    assert client.post("/api/auth/login", json={"email": email}).status_code == 200


def scope(conn, role):
    return scope_for(conn, conn.execute("SELECT id FROM staff_user WHERE role = ?", (role,)).fetchone()["id"])


# ---------------------------------------------------------------- catálogo y reglas

def test_catalog_has_five_tests_of_eight_blocks_and_pulse():
    cat = get_catalog()
    assert list(cat.tests) == ["T01", "T02", "T03", "T04", "T05"]
    for t in cat.tests.values():
        assert len(t.blocks) == 8 and all(len(b["items"]) == 3 for b in t.blocks)
        assert len(t.active_items) == 24
    assert len([i for i in cat.tests["T01"].items if not i.active]) == 4      # reservas T01R01–R04
    assert [p.item_id for p in cat.pulse][:4] == ["F01", "F02", "F03", "F04"] and len(cat.pulse) == 12
    assert cat.tests["T05"].scale_id == "NUM_1_5"


def test_parse_raw_follows_design_rules():
    assert parse_raw("4", 1, 5) == ("num", 4)
    assert parse_raw("NV", 1, 5) == ("nv", None)
    assert parse_raw("", 1, 5) == ("blank", None)
    assert parse_raw("7", 1, 5)[0] == "bad"
    assert parse_raw("3.5", 1, 5)[0] == "bad"
    assert parse_raw("0", 0, 10) == ("num", 0)       # eNPS: 0 es válido


def test_block_needs_two_of_three_and_summary_six_of_eight():
    t = get_catalog().tests["T01"]
    values = {i.item_id: 4 for i in t.active_items}
    b1 = t.blocks[0]["items"]
    values[b1[0]] = None
    values[b1[1]] = None                              # bloque 1 con 1 de 3 → sin calcular
    blocks, media = block_scores(t, values)
    assert blocks[0][1] is None and media == 4
    for b in t.blocks[1:3]:
        for iid in b["items"][:2]:
            values[iid] = None                        # 3 bloques sin calcular → 5 de 8
    blocks, media = block_scores(t, values)
    assert sum(1 for _, s, _ in blocks if s is not None) == 5 and media is None


def test_round_half_up():
    assert round_half_up(2.345) == 2.35
    assert round_half_up(3.3333) == 3.33


def test_quality_control_flags_seeded_errors(conn):
    rows = dict(conn.execute("SELECT control, COUNT(*) FROM evaluation WHERE test_code='T01' AND periodo='2026-10' "
                             "GROUP BY control").fetchall())
    assert rows["METADATOS"] == 1 and rows["DUPLICADO"] == 2 and rows["VALOR_INVALIDO"] == 1
    # Las filas excluidas no entran en el cuadro.
    d = build(conn, get_catalog(), scope(conn, "admin"), "persona", resolve_filters(conn, scope(conn, "admin"), "persona", {}))
    assert d["profiles"]["T01"]["n"] == rows["OK"]


# ---------------------------------------------------------------- cuadros

def test_all_seven_dashboards_build_for_admin(conn):
    s = scope(conn, "admin")
    for key in DASHBOARDS:
        d = build(conn, get_catalog(), s, key, resolve_filters(conn, s, key, {}))
        assert d["kpis"] and set(d["profiles"]) == set(DASHBOARDS[key]["tests"])
        assert d["pulse"]["items"]["F01"]["n"] >= MIN_GROUP


def test_group_below_minimum_is_suppressed(conn):
    s = scope(conn, "admin")
    d = build(conn, get_catalog(), s, "equipo", resolve_filters(conn, s, "equipo", {"equipo": "EQ-DIR"}))
    p = d["profiles"]["T02"]
    assert p["status"] == "MUESTRA INSUFICIENTE" and p["media"] is None
    assert all(b["mean"] is None for b in p["blocks"])
    assert d["pulse"]["enps"]["score"] is None


def test_individual_view_uses_minimum_one_and_shows_items(conn):
    s = scope(conn, "participante")
    d = build(conn, get_catalog(), s, "persona_ia", resolve_filters(conn, s, "persona_ia", {}))
    assert d["individual"] and d["min_n"] == 1
    assert d["profiles"]["T01"]["n"] == 1 and d["profiles"]["T05"]["n"] == 1
    assert set(d["extras"]["items"]) == {"T01", "T05"}
    assert len(d["extras"]["bridges"]) == 6
    # El control de calidad solo cuenta sus propias capturas.
    assert sum(d["quality"]["T01"].values()) == 1


def test_leader_perception_comes_from_own_reports_with_minimum(conn):
    s = scope(conn, "lider")
    d = build(conn, get_catalog(), s, "liderazgo", resolve_filters(conn, s, "liderazgo", {}))
    members = {r[0] for r in conn.execute("SELECT id FROM person WHERE responsable_id = ?", (s.persona_id,))}
    assert d["pulse"]["n"] <= len(members)
    received = d["extras"]["received"]
    assert all((r["mean"] is None) == (r["n"] < MIN_GROUP) for r in received)


def test_leader_ia_compares_with_team_t05(conn):
    s = scope(conn, "lider")
    d = build(conn, get_catalog(), s, "liderazgo_ia", resolve_filters(conn, s, "liderazgo_ia", {}))
    assert d["extras"]["reference"]["label"] == "IA de mi equipo"
    assert d["extras"]["reference"]["n"] >= MIN_GROUP


def test_organization_five_profiles_have_own_n_and_no_global(conn):
    s = scope(conn, "rrhh")
    d = build(conn, get_catalog(), s, "organizacion", resolve_filters(conn, s, "organizacion", {}))
    five = d["extras"]["five_profiles"]
    assert [p["test"] for p in five] == ["T01", "T02", "T03", "T04", "T05"]
    assert len({p["n_data"] for p in five}) > 1          # T03 solo líderes: n distinto
    assert all(not t["visible"] or t["n"] >= MIN_GROUP for t in d["extras"]["teams"]["rows"])


def test_evolution_needs_two_comparable_periods(conn):
    s = scope(conn, "admin")
    d = build(conn, get_catalog(), s, "organizacion", resolve_filters(conn, s, "organizacion", {"organizacion": "ORG-DC"}))
    evo = d["evolution"]["T04"]
    assert evo["available"] and [p["periodo"] for p in evo["series"]] == ["2026-04", "2026-10"]


def test_profile_strengths_and_areas_are_relative():
    t = get_catalog().tests["T01"]
    rows = [{"blocks": {i: float(i % 5) + 1 for i in range(1, 9)}, "media_descriptiva": 3.0, "answers": {}}]
    p = profile(t, rows, 1)
    assert p["strengths"][0]["mean"] >= p["areas"][0]["mean"]


# ---------------------------------------------------------------- permisos

@pytest.mark.parametrize("role,key,raw", [
    ("participante", "persona", {"persona": "DC-PRO-04"}),
    ("participante", "equipo", {}),
    ("rrhh", "persona", {"persona": "DC-PRO-04"}),
    ("consultor", "ia", {"organizacion": "ORG-DI"}),
    ("lider", "equipo", {"equipo": "EQ-VEN"}),
    ("lider", "organizacion", {}),
])
def test_forbidden_scopes(conn, role, key, raw):
    with pytest.raises(Forbidden):
        resolve_filters(conn, scope(conn, role), key, raw)


def test_gestor_has_no_access(client):
    login(client, "gestor@agileinstitute.es")
    assert client.get("/api/auth/me").json()["dashboards"] == []
    assert client.get("/api/dashboard/persona").status_code == 403


def test_leader_is_locked_to_self(client):
    login(client, "lider@democorp.demo")
    d = client.get("/api/dashboard/liderazgo").json()
    assert d["filters"]["persona"] == "DC-PRO-01" and "persona" in d["filters"]["locked"]
    assert client.get("/api/dashboard/liderazgo?persona=DC-VEN-01").status_code == 403


# ---------------------------------------------------------------- API: plan, exportación, importación

def test_plan_save_permissions_and_audit(client, conn):
    login(client, "participante@democorp.demo")
    body = {"objetivo": "Practicar la repriorización", "actions": [{"plazo": "30 días", "accion": "Definir criterios", "estado": "En curso"}]}
    r = client.put("/api/dashboard/persona/plan", json=body)
    assert r.status_code == 200 and r.json()["actions"][0]["estado"] == "En curso"
    assert client.get("/api/dashboard/persona").json()["plan"]["objetivo"] == "Practicar la repriorización"
    login(client, "rrhh@democorp.demo")
    assert client.put("/api/dashboard/equipo/plan", json=body).status_code == 403
    assert conn.execute("SELECT COUNT(*) FROM audit_event WHERE action = 'plan.save'").fetchone()[0] >= 1


def test_export_xlsx_and_item_level_requires_admin_reason(client):
    login(client, "consultor@agileinstitute.es")
    r = client.get("/api/dashboard/ia/export.xlsx")
    assert r.status_code == 200
    wb = openpyxl.load_workbook(io.BytesIO(r.content))
    assert wb.sheetnames == ["Cuadro", "Pulso", "Detalle", "Trazabilidad"]
    assert client.get("/api/dashboard/ia/export.xlsx?include_data=true&reason=verificacion%20manual").status_code == 403
    login(client, "admin@agileinstitute.es")
    assert client.get("/api/dashboard/ia/export.xlsx?include_data=true&reason=corto").status_code == 400
    r = client.get("/api/dashboard/persona_ia/export.xlsx?include_data=true&reason=verificacion%20manual%20PA")
    wb = openpyxl.load_workbook(io.BytesIO(r.content))
    assert "Datos_T01" in wb.sheetnames and "Datos_T05" in wb.sheetnames


def test_import_roundtrip_real_data(tmp_path):
    cat = get_catalog()
    c = db.connect(str(tmp_path / "imp.db"))
    db.init_schema(c)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos_T05"
    meta = ["evaluacion_id", "persona_id", "organizacion_id", "equipo_id", "periodo", "tipo_datos", "fecha_iso"]
    ws.append(meta + [i.item_id for i in cat.tests["T05"].active_items])
    for n in range(6):
        ws.append([f"E{n}", f"P{n}", "ORG-X", "EQ-X", "2026-11", "REAL", "2026-11-05"] + [4] * 24)
    ws.append(["E0", "P9", "ORG-X", "EQ-X", "2026-11", "REAL", "2026-11-05"] + [4] * 24)   # evaluacion_id repetido
    path = tmp_path / "captura.xlsx"
    wb.save(path)
    rep = import_workbook(c, str(path), cat)
    assert rep["rows"]["T05"] == 7
    assert rep["controls"]["T05"] == {"OK": 5, "DUPLICADO": 2}
    f = Filters(tipo="REAL", periodo="2026-11")
    from app.dashboard import fetch_evals
    p = profile(cat.tests["T05"], fetch_evals(c, cat.tests["T05"], f), MIN_GROUP)
    assert p["status"] == "PERFIL DISPONIBLE" and p["media"] == 4


# ---------------------------------------------------------------- distribución personalizada

def test_layout_save_reset_and_isolation_between_users(client):
    login(client, "participante@democorp.demo")
    assert client.get("/api/dashboard/persona").json()["layout"] is None
    body = {"order": ["plan", "kpi-1", "competencias"], "spans": {"plan": 6, "radar": 12}, "hidden": ["calidad"]}
    r = client.put("/api/layout/persona", json=body)
    assert r.status_code == 200 and r.json()["layout"]["hidden"] == ["calidad"]
    assert client.get("/api/dashboard/persona").json()["layout"]["order"][0] == "plan"
    # Otro usuario no ve la distribución del participante.
    login(client, "admin@agileinstitute.es")
    assert client.get("/api/dashboard/persona").json()["layout"] is None
    login(client, "participante@democorp.demo")
    assert client.delete("/api/layout/persona").json() == {"layout": None}
    assert client.get("/api/layout/persona").json()["layout"] is None


@pytest.mark.parametrize("body", [
    {"order": ["plan"], "spans": {"plan": 5}},              # ancho fuera de la rejilla
    {"order": ["<script>"]},                                # identificador no válido
    {"order": "plan"},                                      # tipo incorrecto
    {"order": [f"p{i}" for i in range(61)]},                # demasiados paneles
])
def test_layout_validation(client, body):
    login(client, "admin@agileinstitute.es")
    assert client.put("/api/layout/persona", json=body).status_code == 400


def test_layout_respects_dashboard_permissions(client):
    login(client, "participante@democorp.demo")
    assert client.put("/api/layout/organizacion", json={"order": []}).status_code == 403
    assert client.put("/api/layout/inexistente", json={"order": []}).status_code == 400
