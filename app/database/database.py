"""
Database Manager for VYOM.

Owns a single SQLite connection: connection lifecycle, raw execution,
and transaction management. Schema and query logic belong to the
Repository layer, not here.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from config.constants import DATABASE_NAME


class Database:
    """Thin, transaction-safe wrapper around a SQLite connection."""

    def __init__(self, database_path: str | Path | None = None) -> None:
        if database_path is None:
            database_path = Path("data") / DATABASE_NAME

        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Open the connection lazily on first use."""
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False,
            )
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")

        return self.connection

    def cursor(self) -> sqlite3.Cursor:
        return self.connect().cursor()

    def commit(self) -> None:
        if self.connection:
            self.connection.commit()

    def rollback(self) -> None:
        if self.connection:
            self.connection.rollback()

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Cursor]:
        """Run a block of statements atomically; rolls back on error."""
        cursor = self.cursor()
        try:
            yield cursor
            self.commit()
        except Exception:
            self.rollback()
            raise

    def execute(self, query: str, parameters: tuple = ()) -> sqlite3.Cursor:
        cursor = self.cursor()
        try:
            cursor.execute(query, parameters)
            self.commit()
        except Exception:
            self.rollback()
            raise
        return cursor

    def executemany(self, query: str, parameters: list[tuple]) -> None:
        cursor = self.cursor()
        try:
            cursor.executemany(query, parameters)
            self.commit()
        except Exception:
            self.rollback()
            raise

    def fetchone(self, query: str, parameters: tuple = ()) -> sqlite3.Row | None:
        cursor = self.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchone()

    def fetchall(self, query: str, parameters: tuple = ()) -> list[sqlite3.Row]:
        cursor = self.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()