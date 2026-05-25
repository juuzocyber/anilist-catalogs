"""
Durable SQLite-backed storage for authenticated AniList install keys.

Each auth key maps to one encrypted AniList access token plus optional
encrypted OpenRouter state. The auth key itself is what travels in the
manifest URL path and in configure-page API calls as the ``session`` field.
"""

from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from settings import AUTH_DB_PATH


class AuthStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path).expanduser()
        self._initialized = False

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _connection(self):
        conn = self._connect()
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self) -> None:
        if self._initialized:
            return
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS auth_records (
                    auth_key TEXT PRIMARY KEY,
                    encrypted_anilist_token TEXT NOT NULL,
                    encrypted_openrouter_key TEXT,
                    openrouter_model TEXT,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL,
                    last_used_at INTEGER NOT NULL
                )
                """
            )
            conn.commit()
        self._initialized = True

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            self.initialize()

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        return {
            "auth_key": row["auth_key"],
            "encrypted_anilist_token": row["encrypted_anilist_token"],
            "encrypted_openrouter_key": row["encrypted_openrouter_key"],
            "openrouter_model": row["openrouter_model"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "last_used_at": row["last_used_at"],
        }

    def upsert_auth(
        self,
        auth_key: str,
        encrypted_anilist_token: str,
        *,
        encrypted_openrouter_key: str | None = None,
        openrouter_model: str | None = None,
    ) -> None:
        self._ensure_initialized()
        now = int(time.time())
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO auth_records (
                    auth_key,
                    encrypted_anilist_token,
                    encrypted_openrouter_key,
                    openrouter_model,
                    created_at,
                    updated_at,
                    last_used_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(auth_key) DO UPDATE SET
                    encrypted_anilist_token = excluded.encrypted_anilist_token,
                    encrypted_openrouter_key = excluded.encrypted_openrouter_key,
                    openrouter_model = excluded.openrouter_model,
                    updated_at = excluded.updated_at,
                    last_used_at = excluded.last_used_at
                """,
                (
                    auth_key,
                    encrypted_anilist_token,
                    encrypted_openrouter_key,
                    openrouter_model,
                    now,
                    now,
                    now,
                ),
            )
            conn.commit()

    def get_auth(self, auth_key: str, *, touch_last_used: bool = False) -> dict[str, Any] | None:
        self._ensure_initialized()
        now = int(time.time())
        with self._connection() as conn:
            row = conn.execute(
                """
                SELECT
                    auth_key,
                    encrypted_anilist_token,
                    encrypted_openrouter_key,
                    openrouter_model,
                    created_at,
                    updated_at,
                    last_used_at
                FROM auth_records
                WHERE auth_key = ?
                """,
                (auth_key,),
            ).fetchone()
            if row is None:
                return None
            record = self._row_to_dict(row)
            if touch_last_used and record is not None:
                conn.execute(
                    "UPDATE auth_records SET last_used_at = ? WHERE auth_key = ?",
                    (now, auth_key),
                )
                conn.commit()
                record["last_used_at"] = now
            return record

    def update_openrouter(
        self,
        auth_key: str,
        *,
        encrypted_openrouter_key: str | None,
        openrouter_model: str | None,
    ) -> None:
        self._ensure_initialized()
        now = int(time.time())
        with self._connection() as conn:
            conn.execute(
                """
                UPDATE auth_records
                SET encrypted_openrouter_key = ?,
                    openrouter_model = ?,
                    updated_at = ?,
                    last_used_at = ?
                WHERE auth_key = ?
                """,
                (
                    encrypted_openrouter_key,
                    openrouter_model,
                    now,
                    now,
                    auth_key,
                ),
            )
            conn.commit()

    def delete_auth(self, auth_key: str) -> None:
        self._ensure_initialized()
        with self._connection() as conn:
            conn.execute("DELETE FROM auth_records WHERE auth_key = ?", (auth_key,))
            conn.commit()


auth_store = AuthStore(AUTH_DB_PATH)
