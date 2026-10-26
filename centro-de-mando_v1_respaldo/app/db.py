"""SQLite persistence for the Centro de Test MVP (entities from section 5 of the functional document)."""
import os
import sqlite3

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "centro_test.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active'
);
CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY,
    user_code TEXT NOT NULL UNIQUE,
    company_id INTEGER NOT NULL REFERENCES company(id),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT NOT NULL,
    dimension TEXT,
    email TEXT NOT NULL UNIQUE,
    language TEXT DEFAULT 'es',
    status TEXT NOT NULL DEFAULT 'active',
    consent_status TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS test_definition (
    test_code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    status TEXT,
    purpose TEXT,
    scale_code TEXT,
    expiry_days INTEGER DEFAULT 30,
    reminder_days INTEGER DEFAULT 3,
    ai_report_enabled INTEGER DEFAULT 0,
    license_status TEXT
);
CREATE TABLE IF NOT EXISTS test_indicator (
    test_code TEXT NOT NULL REFERENCES test_definition(test_code),
    indicator_code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    display_order INTEGER,
    weight REAL DEFAULT 1,
    min_score REAL,
    max_score REAL,
    active INTEGER DEFAULT 1,
    PRIMARY KEY (test_code, indicator_code)
);
CREATE TABLE IF NOT EXISTS test_item (
    item_code TEXT NOT NULL,
    test_code TEXT NOT NULL REFERENCES test_definition(test_code),
    indicator_code TEXT NOT NULL,
    item_text TEXT NOT NULL,
    scale_code TEXT,
    display_order INTEGER,
    required INTEGER DEFAULT 1,
    reverse_scored INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1,
    PRIMARY KEY (test_code, item_code)
);
CREATE TABLE IF NOT EXISTS response_option (
    scale_code TEXT NOT NULL,
    value INTEGER NOT NULL,
    label TEXT,
    PRIMARY KEY (scale_code, value)
);
CREATE TABLE IF NOT EXISTS scoring_rule (
    rule_code TEXT PRIMARY KEY,
    test_code TEXT NOT NULL,
    level TEXT NOT NULL,
    target_code TEXT,
    formula_type TEXT,
    weight REAL,
    round_decimals INTEGER,
    scoring_version TEXT,
    active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS interpretation_rule (
    interpretation_code TEXT PRIMARY KEY,
    test_code TEXT NOT NULL,
    target_code TEXT NOT NULL,
    min_score REAL NOT NULL,
    max_score REAL NOT NULL,
    level_name TEXT NOT NULL,
    approved_text TEXT,
    recommended_action TEXT,
    active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS invitation (
    id INTEGER PRIMARY KEY,
    invitation_code TEXT NOT NULL UNIQUE,
    person_id INTEGER NOT NULL REFERENCES person(id),
    test_code TEXT NOT NULL REFERENCES test_definition(test_code),
    test_version TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    reminder_sent_at TEXT,
    completed_at TEXT,
    report_allowed INTEGER DEFAULT 1,
    report_status TEXT DEFAULT 'not_created'
);
CREATE TABLE IF NOT EXISTS response (
    invitation_id INTEGER NOT NULL REFERENCES invitation(id),
    item_code TEXT NOT NULL,
    value INTEGER,
    answered_at TEXT,
    PRIMARY KEY (invitation_id, item_code)
);
CREATE TABLE IF NOT EXISTS result (
    invitation_id INTEGER NOT NULL REFERENCES invitation(id),
    target_code TEXT NOT NULL,
    score REAL,
    level_name TEXT,
    test_version TEXT NOT NULL,
    scoring_version TEXT NOT NULL,
    computed_at TEXT NOT NULL,
    PRIMARY KEY (invitation_id, target_code)
);
CREATE TABLE IF NOT EXISTS email_log (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    invitation_id INTEGER REFERENCES invitation(id),
    recipient TEXT NOT NULL,
    result TEXT NOT NULL,
    provider TEXT,
    sent_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_event (
    id INTEGER PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    entity TEXT,
    at TEXT NOT NULL,
    detail TEXT
);
CREATE TABLE IF NOT EXISTS staff_user (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','gestor','consultor','visor'))
);
CREATE TABLE IF NOT EXISTS staff_company_access (
    staff_id INTEGER NOT NULL REFERENCES staff_user(id),
    company_id INTEGER NOT NULL REFERENCES company(id),
    PRIMARY KEY (staff_id, company_id)
);
CREATE TABLE IF NOT EXISTS dashboard_share (
    staff_id INTEGER NOT NULL REFERENCES staff_user(id),
    company_id INTEGER NOT NULL REFERENCES company(id),
    test_code TEXT NOT NULL REFERENCES test_definition(test_code),
    PRIMARY KEY (staff_id, company_id, test_code)
);
CREATE INDEX IF NOT EXISTS ix_inv_test ON invitation(test_code);
CREATE INDEX IF NOT EXISTS ix_inv_person ON invitation(person_id);
CREATE INDEX IF NOT EXISTS ix_inv_sent ON invitation(sent_at);
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
