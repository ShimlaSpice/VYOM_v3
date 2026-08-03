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
from threading import RLock
from typing import Iterator

from config.constants import DATABASE_NAME


class Database:
    """Thread-safe SQLite database wrapper."""

    def __init__(self, database_path: str | Path | None = None) -> None:

        if database_path is None:

            database_path = Path("data") / DATABASE_NAME

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.connection: sqlite3.Connection | None = None

        self._lock = RLock()

    def connect(self) -> sqlite3.Connection:

        with self._lock:

            if self.connection is None:

                self.connection = sqlite3.connect(

                    self.database_path,

                    check_same_thread=False,

                )

                self.connection.row_factory = sqlite3.Row

                self.connection.execute(

                    "PRAGMA foreign_keys = ON"

                )

                self.connection.execute(

                    "PRAGMA journal_mode=WAL"

                )

                self.connection.execute(

                    "PRAGMA synchronous=NORMAL"

                )

            return self.connection

    def cursor(self) -> sqlite3.Cursor:

        return self.connect().cursor()

    def commit(self) -> None:

        with self._lock:

            if self.connection:

                self.connection.commit()

    def rollback(self) -> None:

        with self._lock:

            if self.connection:

                self.connection.rollback()

    def close(self) -> None:

        with self._lock:

            if self.connection:

                self.connection.close()

                self.connection = None

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Cursor]:

        cursor = self.cursor()

        try:

            yield cursor

            self.commit()

        except Exception:

            self.rollback()

            raise

        finally:

            cursor.close()

    def execute(

        self,

        query: str,

        parameters: tuple = (),

    ) -> sqlite3.Cursor:

        cursor = self.cursor()

        try:

            cursor.execute(

                query,

                parameters,

            )

            self.commit()

            return cursor

        except Exception:

            self.rollback()

            cursor.close()

            raise

    def executemany(

        self,

        query: str,

        parameters: list[tuple],

    ) -> None:

        cursor = self.cursor()

        try:

            cursor.executemany(

                query,

                parameters,

            )

            self.commit()

        except Exception:

            self.rollback()

            raise

        finally:

            cursor.close()

    def fetchone(

        self,

        query: str,

        parameters: tuple = (),

    ) -> sqlite3.Row | None:

        cursor = self.cursor()

        try:

            cursor.execute(

                query,

                parameters,

            )

            return cursor.fetchone()

        finally:

            cursor.close()

    def fetchall(

        self,

        query: str,

        parameters: tuple = (),

    ) -> list[sqlite3.Row]:

        cursor = self.cursor()

        try:

            cursor.execute(

                query,

                parameters,

            )

            return cursor.fetchall()

        finally:

            cursor.close()