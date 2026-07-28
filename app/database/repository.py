"""
Base Repository for VYOM.
"""

from __future__ import annotations

from app.database.database import Database


class Repository:

    def __init__(

        self,

        database: Database,

    ):

        self.database = database

    def execute(

        self,

        query: str,

        parameters: tuple = (),

    ):

        return self.database.execute(

            query,

            parameters,

        )

    def executemany(

        self,

        query: str,

        parameters: list[tuple],

    ):

        self.database.executemany(

            query,

            parameters,

        )

    def fetchone(

        self,

        query: str,

        parameters: tuple = (),

    ):

        return self.database.fetchone(

            query,

            parameters,

        )

    def fetchall(

        self,

        query: str,

        parameters: tuple = (),

    ):

        return self.database.fetchall(

            query,

            parameters,

        )

    def create_table(

        self,

        query: str,

    ):

        self.database.execute(

            query,

        )