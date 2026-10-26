"""Deterministic scoring engine (section 6): compute first, interpret with approved rules after.

Rules come from scoring_rule / interpretation_rule as imported from the Excel master:
- indicator: mean of valid items, reversing items with reverse_scored = true (6 - x on a 1-5 scale).
- global: weighted mean of active indicators.
- rounding per rule.round_decimals, half-up so it matches a manual Excel check (PA-05).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal


def round_half_up(value: float, decimals: int) -> float:
    q = Decimal(1).scaleb(-decimals)
    return float(Decimal(repr(value)).quantize(q, rounding=ROUND_HALF_UP))


def scale_bounds(conn: sqlite3.Connection, scale_code: str) -> tuple[int, int]:
    row = conn.execute(
        "SELECT MIN(value) lo, MAX(value) hi FROM response_option WHERE scale_code = ?", (scale_code,)
    ).fetchone()
    if row is None or row["lo"] is None:
        return 1, 5
    return int(row["lo"]), int(row["hi"])


def scoring_config(conn: sqlite3.Connection, test_code: str) -> dict:
    rules = conn.execute("SELECT * FROM scoring_rule WHERE test_code = ? AND active = 1", (test_code,)).fetchall()
    ind = next((r for r in rules if r["level"] == "indicator"), None)
    glob = next((r for r in rules if r["level"] == "global"), None)
    versions = sorted({r["scoring_version"] for r in rules if r["scoring_version"]})
    return {
        "indicator_decimals": int(ind["round_decimals"]) if ind else 2,
        "global_decimals": int(glob["round_decimals"]) if glob else 2,
        "has_global": glob is not None,
        "scoring_version": versions[-1] if versions else "1.0",
        "configured": ind is not None,
    }


def interpret(conn: sqlite3.Connection, test_code: str, target_code: str, score: float | None) -> str | None:
    if score is None:
        return None
    row = conn.execute(
        """SELECT level_name FROM interpretation_rule
           WHERE test_code = ? AND active = 1 AND target_code IN (?, 'ALL')
             AND ? BETWEEN min_score AND max_score
           ORDER BY CASE WHEN target_code = ? THEN 0 ELSE 1 END LIMIT 1""",
        (test_code, target_code, score, target_code),
    ).fetchone()
    return row["level_name"] if row else None


def compute_result(conn: sqlite3.Connection, invitation_id: int, now: datetime | None = None) -> dict:
    """Compute and persist indicator and global scores for one completed invitation."""
    inv = conn.execute("SELECT * FROM invitation WHERE id = ?", (invitation_id,)).fetchone()
    test_code = inv["test_code"]
    cfg = scoring_config(conn, test_code)
    if not cfg["configured"]:
        raise ValueError(f"El test {test_code} no tiene reglas de puntuación aprobadas.")

    indicators = conn.execute(
        "SELECT * FROM test_indicator WHERE test_code = ? AND active = 1 ORDER BY display_order", (test_code,)
    ).fetchall()
    items = {r["item_code"]: r for r in conn.execute(
        "SELECT * FROM test_item WHERE test_code = ? AND active = 1", (test_code,))}
    answers = conn.execute("SELECT item_code, value FROM response WHERE invitation_id = ?", (invitation_id,)).fetchall()

    per_indicator: dict[str, list[float]] = {i["indicator_code"]: [] for i in indicators}
    for a in answers:
        item = items.get(a["item_code"])
        if item is None or a["value"] is None or item["indicator_code"] not in per_indicator:
            continue
        lo, hi = scale_bounds(conn, item["scale_code"])
        v = float(a["value"])
        if item["reverse_scored"]:
            v = lo + hi - v
        per_indicator[item["indicator_code"]].append(v)

    scores: dict[str, float | None] = {}
    for ind in indicators:
        vals = per_indicator[ind["indicator_code"]]
        scores[ind["indicator_code"]] = round_half_up(sum(vals) / len(vals), cfg["indicator_decimals"]) if vals else None

    global_score = None
    if cfg["has_global"]:
        weighted = [(scores[i["indicator_code"]], i["weight"] or 1) for i in indicators
                    if scores[i["indicator_code"]] is not None]
        if weighted:
            global_score = round_half_up(sum(s * w for s, w in weighted) / sum(w for _, w in weighted),
                                         cfg["global_decimals"])

    computed_at = (now or datetime.now()).isoformat(timespec="seconds")
    conn.execute("DELETE FROM result WHERE invitation_id = ?", (invitation_id,))
    targets = list(scores.items()) + ([("GLOBAL", global_score)] if cfg["has_global"] else [])
    for target, score in targets:
        conn.execute(
            "INSERT INTO result VALUES (?,?,?,?,?,?,?)",
            (invitation_id, target, score, interpret(conn, test_code, target, score),
             inv["test_version"], cfg["scoring_version"], computed_at),
        )
    return {"indicators": scores, "global": global_score, "scoring_version": cfg["scoring_version"]}
