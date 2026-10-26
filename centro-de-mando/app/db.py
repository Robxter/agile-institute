"""Persistencia SQLite de los cuadros de mando por dimensión.

Las tablas siguen el libro de diseño de `Mejora/`:
- `evaluation` + `answer`: una fila por persona, cuestionario y periodo (hojas Datos_T01…Datos_T05).
- `pulse` + `pulse_answer`: el pulso de experiencia laboral (hoja Datos_PULSO).
- `action_plan`: el registro manual de seguimiento (hoja M_Acciones), editable desde cada cuadro.
- `user_layout`: la distribución personalizada de los paneles de cada cuadro, por usuario.
Los identificadores de persona son anónimos: no se guardan nombres ni correos de participantes.
"""
import os
import sqlite3

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "centro_mando.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS organization (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS team (
    id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL REFERENCES organization(id),
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS person (
    id TEXT PRIMARY KEY,                       -- identificador anónimo (persona_id)
    organization_id TEXT NOT NULL REFERENCES organization(id),
    team_id TEXT NOT NULL REFERENCES team(id),
    is_leader INTEGER NOT NULL DEFAULT 0,
    responsable_id TEXT                        -- líder directo (persona_id)
);
CREATE TABLE IF NOT EXISTS evaluation (
    id INTEGER PRIMARY KEY,
    evaluacion_id TEXT,
    test_code TEXT NOT NULL,
    persona_id TEXT,
    organizacion_id TEXT,
    equipo_id TEXT,
    periodo TEXT,
    tipo_datos TEXT,
    fecha_iso TEXT,
    test_version TEXT,
    control TEXT,                              -- OK · METADATOS · DUPLICADO · VALOR_INVALIDO
    media_descriptiva REAL,
    n_blocks INTEGER,
    source TEXT
);
CREATE TABLE IF NOT EXISTS answer (
    eval_id INTEGER NOT NULL REFERENCES evaluation(id) ON DELETE CASCADE,
    item_id TEXT NOT NULL,
    raw TEXT NOT NULL,                         -- '1'..'5', 'NV' (no observable) u otro valor (inválido)
    PRIMARY KEY (eval_id, item_id)
);
CREATE TABLE IF NOT EXISTS block_score (
    eval_id INTEGER NOT NULL REFERENCES evaluation(id) ON DELETE CASCADE,
    block INTEGER NOT NULL,
    score REAL,
    n_valid INTEGER NOT NULL,
    PRIMARY KEY (eval_id, block)
);
CREATE TABLE IF NOT EXISTS pulse (
    id INTEGER PRIMARY KEY,
    evaluacion_id TEXT,
    persona_id TEXT,
    organizacion_id TEXT,
    equipo_id TEXT,
    periodo TEXT,
    tipo_datos TEXT,
    fecha_iso TEXT,
    responsable_id TEXT,
    control TEXT,
    source TEXT
);
CREATE TABLE IF NOT EXISTS pulse_answer (
    pulse_id INTEGER NOT NULL REFERENCES pulse(id) ON DELETE CASCADE,
    item_id TEXT NOT NULL,
    raw TEXT NOT NULL,
    PRIMARY KEY (pulse_id, item_id)
);
CREATE TABLE IF NOT EXISTS action_plan (
    id INTEGER PRIMARY KEY,
    dashboard TEXT NOT NULL,
    scope_key TEXT NOT NULL,                   -- tipo|periodo|organización|equipo|persona
    objetivo TEXT,
    actions TEXT NOT NULL DEFAULT '[]',        -- JSON: [{plazo, accion, responsable, fecha_limite, estado, evidencia}]
    updated_by TEXT,
    updated_at TEXT,
    UNIQUE (dashboard, scope_key)
);
CREATE TABLE IF NOT EXISTS staff_user (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','consultor','rrhh','lider','participante','gestor')),
    persona_id TEXT REFERENCES person(id),
    organization_id TEXT REFERENCES organization(id)
);
CREATE TABLE IF NOT EXISTS staff_org_access (
    staff_id INTEGER NOT NULL REFERENCES staff_user(id),
    organization_id TEXT NOT NULL REFERENCES organization(id),
    PRIMARY KEY (staff_id, organization_id)
);
CREATE TABLE IF NOT EXISTS user_layout (
    staff_id INTEGER NOT NULL REFERENCES staff_user(id),
    dashboard TEXT NOT NULL,
    layout TEXT NOT NULL,                      -- JSON: {"order": [ids], "spans": {id: columnas}, "hidden": [ids]}
    updated_at TEXT NOT NULL,
    PRIMARY KEY (staff_id, dashboard)
);
CREATE TABLE IF NOT EXISTS audit_event (
    id INTEGER PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    entity TEXT,
    at TEXT NOT NULL,
    detail TEXT
);
CREATE INDEX IF NOT EXISTS ix_eval_cut ON evaluation(test_code, tipo_datos, periodo);
CREATE INDEX IF NOT EXISTS ix_pulse_cut ON pulse(tipo_datos, periodo);
"""


def connect(path: str | None = None) -> sqlite3.Connection:
    path = path or os.environ.get("CDM_DB_PATH", DEFAULT_DB_PATH)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()
