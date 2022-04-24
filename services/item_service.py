import aiosqlite
from models.item import Item
from repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor

        self._user_repository = ItemRepository(self._connection, self._cursor)

    async def get_all(self) -> list[Item | None]:
        return await self._user_repository.get_all()

    async def get(self, id: int) -> Item:
        return await self._user_repository.get(id)

    async def add(self, entity: Item) -> None:
        await self._user_repository.add(entity)
        await self._user_repository.save_changes()

    async def update(self, entity: Item) -> None:
        await self._user_repository.update(entity)
        await self._user_repository.save_changes()

    async def delete(self, entity: Item) -> None:
        await self._user_repository.delete(entity)
        await self._user_repository.save_changes()
