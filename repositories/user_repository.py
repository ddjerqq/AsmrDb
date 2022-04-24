import aiosqlite
from models.user import User


class UserRepository:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[User | None]:
        await self._cursor.execute("SELECT * FROM users")
        data = await self._cursor.fetchall()
        return [User.from_db(i) for i in data]

    async def get(self, id: int) -> User | None:
        await self._cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        data = await self._cursor.fetchone()
        return None if data is None else User.from_db(data)

    async def add(self, entity: User) -> None:
        await self._cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)",
                                   entity.to_db)

    async def update(self, entity: User) -> None:
        await self._cursor.execute("""
        UPDATE users
        SET username=?, experience=?, wallet=?, bank=?
        WHERE id=?""", (entity.username, entity.experience, entity.wallet, entity.bank, entity.id))

    async def delete(self, entity: User) -> None:
        await self._cursor.execute("""
        DELETE FROM users
        WHERE id=?
        """, (entity.id,))
