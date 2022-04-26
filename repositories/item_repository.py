import aiosqlite
from models.item import Item


class ItemRepository:
    def __init__(self, conn: aiosqlite.Connection, curs: aiosqlite.Cursor):
        self._connection = conn
        self._cursor     = curs

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Item | None]:
        await self._cursor.execute("SELECT * FROM items")
        data = await self._cursor.fetchall()
        return [Item.from_db(i) for i in data]

    async def get(self, id: int) -> Item | None:
        await self._cursor.execute("SELECT * FROM items WHERE id=?", (id,))
        data = await self._cursor.fetchone()
        return None if data is None else Item.from_db(data)

    async def add(self, entity: Item) -> None:
        await self._cursor.execute("INSERT INTO items VALUES(?, ?, ?, ?)",
                                   entity.to_db)

    async def update(self, entity: Item) -> None:
        await self._cursor.execute("""
        UPDATE items
        SET type=?, rarity=?, owner_id=?
        WHERE id=?""", (entity.type, entity.rarity, entity.owner_id, entity.id))

    async def delete(self, entity: Item) -> None:
        await self._cursor.execute("""
        DELETE FROM items
        WHERE id=?
        """, (entity.id,))
