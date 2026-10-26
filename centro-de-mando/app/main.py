"""API FastAPI: cuadros de mando por dimensión profesional (Persona, Equipo, Liderazgo, Organización,
IA transversal, Persona + IA y Líder + IA).

Arranque:  python -m uvicorn app.main:app --port 8765   (la base se construye sola en el primer arranque)
"""
from __future__ import annotations

import json
import os
import secrets
import sqlite3
import tempfile
import threading
from datetime import datetime

from fastapi import Body, Depends, FastAPI, File, HTTPException, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db
from .catalog import get_catalog
from .dashboard import (DASHBOARDS, ROLE_LABELS, BadRequest, Forbidden, Scope, build, data_rows, layout_get, layout_reset,
                        layout_save, options, overview, plan_save, resolve_filters, scope_for)
from .export_xlsx import build_workbook
from .importer import import_workbook
from .seed import build_database

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
SESSION_COOKIE = "cdm_session"

_lock = threading.Lock()
_sessions: dict[str, int] = {}
_conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    global _conn
    with _lock:
        if _conn is None:
            path = os.environ.get("CDM_DB_PATH", db.DEFAULT_DB_PATH)
            if not os.path.exists(path):
                _conn, _ = build_database(path)
            else:
                _conn = db.connect(path)
                db.init_schema(_conn)
        return _conn


def set_connection(conn: sqlite3.Connection) -> None:
    """Para las pruebas: inyecta una base aislada."""
    global _conn
    _conn = conn
    _sessions.clear()


def audit(conn: sqlite3.Connection, actor: str, action: str, entity: str, detail: dict) -> None:
    conn.execute("INSERT INTO audit_event(actor, action, entity, at, detail) VALUES (?,?,?,?,?)",
                 (actor, action, entity, datetime.now().isoformat(timespec="seconds"),
                  json.dumps(detail, ensure_ascii=False)))
    conn.commit()


def current_scope(request: Request, conn: sqlite3.Connection = Depends(get_conn)) -> Scope:
    staff_id = _sessions.get(request.cookies.get(SESSION_COOKIE) or "")
    if staff_id is None:
        raise HTTPException(401, "Sesión no iniciada.")
    try:
        return scope_for(conn, staff_id)
    except Forbidden as e:
        raise HTTPException(403, str(e))


def raw_filters(tipo: str | None = Query(None), periodo: str | None = Query(None, pattern=r"^\d{4}-\d{2}$"),
                organizacion: str | None = Query(None), equipo: str | None = Query(None),
                persona: str | None = Query(None)) -> dict:
    return {"tipo": tipo, "periodo": periodo, "organizacion": organizacion, "equipo": equipo, "persona": persona}


def _resolve(conn, scope, key, raw):
    try:
        return resolve_filters(conn, scope, key, raw)
    except Forbidden as e:
        raise HTTPException(403, str(e))
    except BadRequest as e:
        raise HTTPException(400, str(e))


app = FastAPI(title="Cuadros de mando por dimensión · Agile Institute", version="2.0")


class LoginBody(BaseModel):
    email: str


@app.get("/api/auth/demo-accounts")
def demo_accounts(conn: sqlite3.Connection = Depends(get_conn)):
    if os.environ.get("CDM_DEMO_LOGIN", "1") != "1":
        raise HTTPException(404)
    return [dict(r) | {"role_label": ROLE_LABELS[r["role"]]}
            for r in conn.execute("SELECT email, name, role FROM staff_user ORDER BY id")]


@app.post("/api/auth/login")
def login(body: LoginBody, response: Response, conn: sqlite3.Connection = Depends(get_conn)):
    # Acceso de demostración. En producción la autenticación la aporta la plataforma.
    if os.environ.get("CDM_DEMO_LOGIN", "1") != "1":
        raise HTTPException(404)
    row = conn.execute("SELECT id, role FROM staff_user WHERE email = ?", (body.email.strip().lower(),)).fetchone()
    if row is None:
        raise HTTPException(401, "Cuenta no reconocida.")
    token = secrets.token_urlsafe(32)
    _sessions[token] = row["id"]
    response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="strict")
    audit(conn, body.email, "auth.login", "staff_user", {"role": row["role"]})
    return {"ok": True, "role": row["role"]}


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):
    _sessions.pop(request.cookies.get(SESSION_COOKIE, ""), None)
    response.delete_cookie(SESSION_COOKIE)
    return {"ok": True}


@app.get("/api/auth/me")
def me(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    staff_id = _sessions.get(request.cookies.get(SESSION_COOKIE) or "")
    if staff_id is None:
        raise HTTPException(401, "Sesión no iniciada.")
    s = conn.execute("SELECT * FROM staff_user WHERE id = ?", (staff_id,)).fetchone()
    try:
        scope = scope_for(conn, staff_id)
    except Forbidden:
        scope = None
    return {"email": s["email"], "name": s["name"], "role": s["role"], "role_label": ROLE_LABELS[s["role"]],
            "persona_id": s["persona_id"],
            "dashboards": [{"key": k, "label": v["label"]} for k, v in DASHBOARDS.items() if scope and k in scope.dashboards],
            "can_pick_person": bool(scope and scope.can_pick_person),
            "can_export_data": bool(scope and scope.can_export_data),
            "can_import": bool(scope and scope.can_import)}


@app.get("/api/overview")
def get_overview(raw: dict = Depends(raw_filters), scope: Scope = Depends(current_scope),
                 conn: sqlite3.Connection = Depends(get_conn)):
    try:
        return overview(conn, get_catalog(), scope, raw)
    except (Forbidden, BadRequest) as e:
        raise HTTPException(403 if isinstance(e, Forbidden) else 400, str(e))


@app.get("/api/dashboard/{key}")
def get_dashboard(key: str, raw: dict = Depends(raw_filters), scope: Scope = Depends(current_scope),
                  conn: sqlite3.Connection = Depends(get_conn)):
    f = _resolve(conn, scope, key, raw)
    out = build(conn, get_catalog(), scope, key, f)
    out["options"] = options(conn, scope, key, f)
    out["layout"] = layout_get(conn, scope, key)
    return out


@app.put("/api/dashboard/{key}/plan")
def put_plan(key: str, body: dict = Body(...), raw: dict = Depends(raw_filters), scope: Scope = Depends(current_scope),
             conn: sqlite3.Connection = Depends(get_conn)):
    f = _resolve(conn, scope, key, raw)
    try:
        plan = plan_save(conn, scope, key, f, body)
    except Forbidden as e:
        raise HTTPException(403, str(e))
    audit(conn, scope.email, "plan.save", key, {"filters": f.public(), "actions": len(plan["actions"])})
    return plan


@app.get("/api/dashboard/{key}/export.xlsx")
def export_xlsx(key: str, raw: dict = Depends(raw_filters), include_data: bool = False,
                reason: str | None = Query(None, max_length=300), scope: Scope = Depends(current_scope),
                conn: sqlite3.Connection = Depends(get_conn)):
    f = _resolve(conn, scope, key, raw)
    catalog = get_catalog()
    tables = None
    if include_data:
        if not scope.can_export_data:
            raise HTTPException(403, "La exportación de datos ítem a ítem solo está autorizada a administración.")
        if not reason or len(reason.strip()) < 10:
            raise HTTPException(400, "Indica el motivo de la exportación administrativa (mínimo 10 caracteres).")
        tables = data_rows(conn, catalog, scope, key, f)
    data = build(conn, catalog, scope, key, f)
    content = build_workbook(data, scope.email, scope.role, tables, reason.strip() if reason else None)
    audit(conn, scope.email, "dashboard.export_xlsx", key,
          {"filters": f.public(), "item_level": tables is not None, "reason": reason})
    name = f"cuadro_{key}_{f.periodo}_{datetime.now():%Y%m%d_%H%M}.xlsx"
    return StreamingResponse(iter([content]), headers={"Content-Disposition": f'attachment; filename="{name}"'},
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.post("/api/import")
async def post_import(file: UploadFile = File(...), scope: Scope = Depends(current_scope),
                      conn: sqlite3.Connection = Depends(get_conn)):
    if not scope.can_import:
        raise HTTPException(403, "Solo administración puede importar capturas.")
    if not (file.filename or "").lower().endswith(".xlsx"):
        raise HTTPException(400, "Sube un libro .xlsx con hojas Datos_T01…Datos_T05 y/o Datos_PULSO.")
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(await file.read())
        report = import_workbook(conn, path, source=file.filename)
    except ValueError as e:
        raise HTTPException(400, str(e))
    finally:
        os.remove(path)
    audit(conn, scope.email, "data.import", "evaluation", {"file": file.filename, **report})
    return report


def _layout_call(fn, *args):
    try:
        return fn(*args)
    except Forbidden as e:
        raise HTTPException(403, str(e))
    except BadRequest as e:
        raise HTTPException(400, str(e))


@app.get("/api/layout/{key}")
def get_layout(key: str, scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    return {"layout": _layout_call(layout_get, conn, scope, key)}


@app.put("/api/layout/{key}")
def put_layout(key: str, body: dict = Body(...), scope: Scope = Depends(current_scope),
               conn: sqlite3.Connection = Depends(get_conn)):
    return {"layout": _layout_call(layout_save, conn, scope, key, body)}


@app.delete("/api/layout/{key}")
def delete_layout(key: str, scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    """Vuelve a la distribución estándar del cuadro."""
    _layout_call(layout_reset, conn, scope, key)
    return {"layout": None}


@app.get("/api/audit")
def get_audit(scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    if scope.role != "admin":
        raise HTTPException(403, "Solo administración puede consultar la auditoría.")
    return [dict(r) for r in conn.execute("SELECT * FROM audit_event ORDER BY id DESC LIMIT 50")]


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
