import aiosqlite
from models.pet import Pet


class PetRepository:
    def __init__(self, conn: aiosqlite.Connection, curs: aiosqlite.Cursor):
        self._connection = conn
        self._cursor     = curs

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Pet | None]:
        await self._cursor.execute("SELECT * FROM pets")
        data = await self._cursor.fetchall()
        return [Pet.from_db(i) for i in data]

    async def get(self, id: int) -> Pet | None:
        await self._cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
        data = await self._cursor.fetchone()
        return None if data is None else Pet.from_db(data)

    async def add(self, entity: Pet) -> None:
        await self._cursor.execute("INSERT INTO pets VALUES(?, ?, ?, ?, ?)",
                                   entity.to_db)

    async def update(self, entity: Pet) -> None:
        await self._cursor.execute("""
        UPDATE pets
        SET type=?, name=?, experience=?, owner_id=?
        WHERE id=?""", (entity.type, entity.name, entity.experience, entity.owner_id, entity.id))

    async def delete(self, entity: Pet) -> None:
        await self._cursor.execute("""
        DELETE FROM pets
        WHERE id=?
        """, (entity.id,))
