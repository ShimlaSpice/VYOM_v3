"""
Database Manager for VYOM.

Central SQLite database connection.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:

    DATABASE_NAME = "vyom.db"

    def __init__(

        self,

        database_path: str | None = None,

    ):

        if database_path is None:

            database_path = str(

                Path("data") / self.DATABASE_NAME

            )

        self.database_path = database_path

        Path(

            self.database_path

        ).parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.connection: sqlite3.Connection | None = None

    def connect(

        self,

    ) -> sqlite3.Connection:

        if self.connection is None:

            self.connection = sqlite3.connect(

                self.database_path,

                check_same_thread=False,

            )

            self.connection.row_factory = sqlite3.Row

        return self.connection

    def cursor(

        self,

    ) -> sqlite3.Cursor:

        return self.connect().cursor()

    def commit(

        self,

    ) -> None:

        if self.connection:

            self.connection.commit()

    def rollback(

        self,

    ) -> None:

        if self.connection:

            self.connection.rollback()

    def close(

        self,

    ) -> None:

        if self.connection:

            self.connection.close()

            self.connection = None

    def execute(

        self,

        query: str,

        parameters: tuple = (),

    ) -> sqlite3.Cursor:

        cursor = self.cursor()

        cursor.execute(

            query,

            parameters,

        )

        self.commit()

        return cursor

    def executemany(

        self,

        query: str,

        parameters: list[tuple],

    ) -> None:

        cursor = self.cursor()

        cursor.executemany(

            query,

            parameters,

        )

        self.commit()

    def fetchone(

        self,

        query: str,

        parameters: tuple = (),

    ):

        cursor = self.cursor()

        cursor.execute(

            query,

            parameters,

        )

        return cursor.fetchone()

    def fetchall(

        self,

        query: str,

        parameters: tuple = (),

    ):

        cursor = self.cursor()

        cursor.execute(

            query,

            parameters,

        )

        return cursor.fetchall()