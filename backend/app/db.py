"""SQLite persistence for guides, per-client checklist progress and generation jobs."""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .models import Guide, GuideSummary, Job, JobEvent, ProgressState, summarize

SCHEMA = """
CREATE TABLE IF NOT EXISTS guides (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL,
  generated_by TEXT NOT NULL,
  data TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_guides_slug ON guides(slug);
CREATE TABLE IF NOT EXISTS progress (
  guide_id TEXT NOT NULL,
  client_id TEXT NOT NULL,
  checked TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (guide_id, client_id)
);
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  guide_id TEXT NOT NULL,
  query TEXT NOT NULL,
  status TEXT NOT NULL,
  events TEXT NOT NULL,
  error TEXT,
  error_code TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: str):
        self.path = path
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        with self._tx() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _tx(self):
        with self._lock:
            try:
                yield self._conn
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    # ------------------------------------------------------------------ guides
    def save_guide(self, guide: Guide) -> None:
        with self._tx() as c:
            c.execute(
                "INSERT OR REPLACE INTO guides (id, slug, generated_by, data, created_at) VALUES (?,?,?,?,?)",
                (guide.id, guide.slug, guide.generated_by, guide.model_dump_json(), now_iso()),
            )

    def get_guide(self, guide_id: str) -> Guide | None:
        with self._tx() as c:
            row = c.execute("SELECT data FROM guides WHERE id = ?", (guide_id,)).fetchone()
        return Guide.model_validate_json(row["data"]) if row else None

    def find_seed_by_slug(self, slug: str) -> Guide | None:
        with self._tx() as c:
            row = c.execute(
                "SELECT data FROM guides WHERE slug = ? AND generated_by = 'seed' LIMIT 1", (slug,)
            ).fetchone()
        return Guide.model_validate_json(row["data"]) if row else None

    def list_guides(self) -> list[GuideSummary]:
        with self._tx() as c:
            rows = c.execute(
                "SELECT data FROM guides ORDER BY (generated_by = 'seed') DESC, created_at DESC"
            ).fetchall()
        return [summarize(Guide.model_validate_json(r["data"])) for r in rows]

    def count_guides(self) -> int:
        with self._tx() as c:
            return c.execute("SELECT COUNT(*) AS n FROM guides").fetchone()["n"]

    # ---------------------------------------------------------------- progress
    def get_progress(self, guide_id: str, client_id: str) -> ProgressState:
        with self._tx() as c:
            row = c.execute(
                "SELECT checked, updated_at FROM progress WHERE guide_id = ? AND client_id = ?",
                (guide_id, client_id),
            ).fetchone()
        if not row:
            return ProgressState()
        return ProgressState(checked=json.loads(row["checked"]), updated_at=row["updated_at"])

    def merge_progress(self, guide_id: str, client_id: str, updates: dict[str, bool]) -> ProgressState:
        current = self.get_progress(guide_id, client_id).checked
        current.update(updates)
        current = {k: v for k, v in current.items() if v}  # store only checked items
        ts = now_iso()
        with self._tx() as c:
            c.execute(
                "INSERT OR REPLACE INTO progress (guide_id, client_id, checked, updated_at) VALUES (?,?,?,?)",
                (guide_id, client_id, json.dumps(current), ts),
            )
        return ProgressState(checked=current, updated_at=ts)

    # -------------------------------------------------------------------- jobs
    def create_job(self, job_id: str, guide_id: str, query: str) -> Job:
        ts = now_iso()
        with self._tx() as c:
            c.execute(
                "INSERT INTO jobs (id, guide_id, query, status, events, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                (job_id, guide_id, query, "queued", "[]", ts, ts),
            )
        return self.get_job(job_id)  # type: ignore[return-value]

    def get_job(self, job_id: str) -> Job | None:
        with self._tx() as c:
            r = c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not r:
            return None
        return Job(
            id=r["id"],
            guide_id=r["guide_id"],
            query=r["query"],
            status=r["status"],
            events=[JobEvent(**e) for e in json.loads(r["events"])],
            error=r["error"],
            error_code=r["error_code"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
        )

    def add_job_event(self, job_id: str, stage: str, message: str, level: str = "info") -> None:
        with self._tx() as c:
            r = c.execute("SELECT events FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not r:
                return
            events = json.loads(r["events"])
            events.append({"ts": now_iso(), "stage": stage, "message": message, "level": level})
            c.execute("UPDATE jobs SET events = ?, updated_at = ? WHERE id = ?", (json.dumps(events), now_iso(), job_id))

    def set_job_status(self, job_id: str, status: str, error: str | None = None, error_code: str | None = None) -> None:
        with self._tx() as c:
            c.execute(
                "UPDATE jobs SET status = ?, error = ?, error_code = ?, updated_at = ? WHERE id = ?",
                (status, error, error_code, now_iso(), job_id),
            )

    def close(self) -> None:
        self._conn.close()
