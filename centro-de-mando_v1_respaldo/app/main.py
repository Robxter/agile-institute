"""FastAPI application: Centro de mando (menú 5 · Informes y cuadros de mando).

Start:  uvicorn app.main:app --reload     (the database is built from the Excel maestro on first run)
"""
from __future__ import annotations

import json
import os
import secrets
import sqlite3
import threading
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db
from .dashboard import (Filters, Forbidden, Scope, dashboard, filter_options, item_responses, result_rows,
                        scope_for)
from .export_xlsx import build_workbook
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
                _conn, _, _ = build_database(path)
            else:
                _conn = db.connect(path)
                db.init_schema(_conn)
        return _conn


def set_connection(conn: sqlite3.Connection) -> None:
    """Used by tests to inject an isolated database."""
    global _conn
    _conn = conn
    _sessions.clear()


def audit(conn: sqlite3.Connection, actor: str, action: str, entity: str, detail: dict) -> None:
    conn.execute("INSERT INTO audit_event(actor, action, entity, at, detail) VALUES (?,?,?,?,?)",
                 (actor, action, entity, datetime.now().isoformat(timespec="seconds"),
                  json.dumps(detail, ensure_ascii=False)))
    conn.commit()


def current_scope(request: Request, conn: sqlite3.Connection = Depends(get_conn)) -> Scope:
    token = request.cookies.get(SESSION_COOKIE)
    staff_id = _sessions.get(token or "")
    if staff_id is None:
        raise HTTPException(401, "Sesión no iniciada.")
    try:
        return scope_for(conn, staff_id)
    except Forbidden as e:
        raise HTTPException(403, str(e))


def filters_dep(company_id: int | None = Query(None), test_code: str | None = Query(None),
                date_from: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
                date_to: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$")) -> Filters:
    return Filters(company_id=company_id, test_code=test_code or None, date_from=date_from, date_to=date_to)


def check_filters(scope: Scope, f: Filters) -> None:
    """Explicitly requesting an unauthorised company/test is denied rather than silently emptied (PA-10)."""
    if f.company_id and scope.company_ids is not None and f.company_id not in scope.company_ids:
        raise HTTPException(403, "Empresa no autorizada para tu rol.")
    if f.test_code and scope.role == "visor" and f.test_code not in {t for _, t in scope.shares}:
        raise HTTPException(403, "Test no compartido contigo.")


app = FastAPI(title="Centro de mando · Centro de Test", version="1.0")


class LoginBody(BaseModel):
    email: str


@app.get("/api/auth/demo-accounts")
def demo_accounts(conn: sqlite3.Connection = Depends(get_conn)):
    if os.environ.get("CDM_DEMO_LOGIN", "1") != "1":
        raise HTTPException(404)
    return [dict(r) for r in conn.execute("SELECT email, name, role FROM staff_user ORDER BY id")]


@app.post("/api/auth/login")
def login(body: LoginBody, response: Response, conn: sqlite3.Connection = Depends(get_conn)):
    # Demo access only. In production authentication is delegated to the platform (Base44 auth).
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
    s = conn.execute("SELECT email, name, role FROM staff_user WHERE id = ?", (staff_id,)).fetchone()
    try:
        scope = scope_for(conn, staff_id)
        allowed = True
    except Forbidden:
        scope, allowed = None, False
    return {"email": s["email"], "name": s["name"], "role": s["role"], "dashboard_access": allowed,
            "can_see_individuals": bool(scope and scope.can_see_individuals),
            "can_export_items": bool(scope and scope.can_export_items)}


@app.get("/api/filters")
def get_filters(scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    return filter_options(conn, scope)


@app.get("/api/dashboard")
def get_dashboard(f: Filters = Depends(filters_dep), scope: Scope = Depends(current_scope),
                  conn: sqlite3.Connection = Depends(get_conn)):
    check_filters(scope, f)
    return dashboard(conn, scope, f)


@app.get("/api/results")
def get_results(f: Filters = Depends(filters_dep), scope: Scope = Depends(current_scope),
                conn: sqlite3.Connection = Depends(get_conn)):
    check_filters(scope, f)
    try:
        return result_rows(conn, scope, f)
    except Forbidden as e:
        raise HTTPException(403, str(e))


@app.get("/api/export.xlsx")
def export_xlsx(f: Filters = Depends(filters_dep), include_responses: bool = False,
                reason: str | None = Query(None, max_length=300),
                scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    check_filters(scope, f)
    items = None
    if include_responses:
        if not scope.can_export_items:
            raise HTTPException(403, "La exportación de respuestas ítem a ítem solo está autorizada a administración.")
        if not reason or len(reason.strip()) < 10:
            raise HTTPException(400, "Indica el motivo de la exportación administrativa (mínimo 10 caracteres).")
        items = item_responses(conn, scope, f)
    data = dashboard(conn, scope, f)
    table = result_rows(conn, scope, f) if scope.can_see_individuals else None
    content = build_workbook(data, table, items, actor=scope.email, reason=reason.strip() if reason else None)
    # Section 15: exports are recorded.
    audit(conn, scope.email, "dashboard.export_xlsx", "dashboard",
          {"filters": data["filters"], "item_level": items is not None, "reason": reason,
           "rows": len(table["rows"]) if table else 0})
    name = f"centro_de_mando_{datetime.now():%Y%m%d_%H%M}.xlsx"
    return StreamingResponse(iter([content]), headers={"Content-Disposition": f'attachment; filename="{name}"'},
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/api/audit")
def get_audit(scope: Scope = Depends(current_scope), conn: sqlite3.Connection = Depends(get_conn)):
    if scope.role != "admin":
        raise HTTPException(403, "Solo administración puede consultar la auditoría.")
    return [dict(r) for r in conn.execute("SELECT * FROM audit_event ORDER BY id DESC LIMIT 50")]


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
