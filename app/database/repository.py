"""
Base Repository for VYOM.

Shared query plumbing, plus a generic dataclass-driven insert helper so
concrete repositories don't hand-write column lists and positional
parameter tuples for every INSERT statement.
"""

from __future__ import annotations

import sqlite3
from dataclasses import fields
from typing import Any

from app.database.database import Database


class Repository:
    """Base class for all repositories."""

    def __init__(self, database: Database) -> None:

        self.database = database

    def execute(

        self,

        query: str,

        parameters: tuple = (),

    ) -> sqlite3.Cursor:

        return self.database.execute(

            query,

            parameters,

        )

    def executemany(

        self,

        query: str,

        parameters: list[tuple],

    ) -> None:

        self.database.executemany(

            query,

            parameters,

        )

    def fetchone(

        self,

        query: str,

        parameters: tuple = (),

    ) -> sqlite3.Row | None:

        return self.database.fetchone(

            query,

            parameters,

        )

    def fetchall(

        self,

        query: str,

        parameters: tuple = (),

    ) -> list[sqlite3.Row]:

        return self.database.fetchall(

            query,

            parameters,

        )

    def create_table(

        self,

        query: str,

    ) -> None:

        self.execute(

            query,

        )

    def _insert(

        self,

        table: str,

        record: Any,

        exclude: tuple[str, ...] = (

            "id",

        ),

    ) -> int:

        data = {

            field.name: getattr(

                record,

                field.name,

            )

            for field in fields(

                record,

            )

            if field.name not in exclude

        }

        columns = ", ".join(

            data.keys(),

        )

        placeholders = ", ".join(

            "?"

            for _ in data

        )

        cursor = self.execute(

            f"""

            INSERT INTO {table}

            ({columns})

            VALUES

            ({placeholders})

            """,

            tuple(

                data.values(),

            ),

        )

        return int(

            cursor.lastrowid,

        )

    @staticmethod
    def _row_to_kwargs(

        row: sqlite3.Row,

    ) -> dict[str, Any]:

        return dict(

            row,

        )