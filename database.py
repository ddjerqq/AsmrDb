from __future__ import annotations

import os
import asyncio
import aiosqlite

from services.user_service import UserService


class AsmrDb(object):
    """
    Async Service Model Repository Database
    ---------------------------------------

    initialize the database like so: \n
    >>> db = await AsmrDb.new()

    then you can access items and users with
    >>> user  = await db.users.get(snowflake)
    """
    _DB_PATH = os.path.dirname(os.path.realpath(__file__)) + "/database.db"

    def __init__(self, conn: aiosqlite.Connection, curs: aiosqlite.Cursor):
        self._connection  = conn
        self._cursor      = curs
        self.users = UserService(conn, curs)

    @classmethod
    async def new(cls):
        """|coro|
        Initialize the database asynchronously"""
        conn = await aiosqlite.connect(cls._DB_PATH)
        curs = await conn.cursor()
        return cls(conn, curs)
