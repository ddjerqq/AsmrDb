import aiosqlite
from models.user import User
from repositories.user_repository import UserRepository
from repositories.item_repository import ItemRepository


class UserService:
    def __init__(self, conn: aiosqlite.Connection, curs: aiosqlite.Cursor):
        self._connection = conn
        self._cursor = curs
        self._user_repository = UserRepository(conn, curs)
        self._item_repository = ItemRepository(conn, curs)


    async def get_all(self):
        items = await self._item_repository.get_all()
        users = await self._user_repository.get_all()

        for user in users:
            user.items = list(filter(lambda i: i.owner_id == user.id, items))

        return users


    async def get(self, id: int) -> User:
        items = await self._item_repository.get_all()
        items = list(filter(lambda i: i.owner_id == id, items))

        entity = await self._user_repository.get(id)
        entity.items = items

        return entity

    async def add(self, entity: User) -> None:
        await self._user_repository.add(entity)
        for item in entity.items:
            await self._item_repository.add(item)
        await self._user_repository.save_changes()

    async def update(self, entity: User) -> None:
        await self._user_repository.update(entity)
        await self._user_repository.save_changes()

        old = await self._item_repository.get_all()
        old = filter(lambda i: i.owner_id == entity.id, old)

        new = set(entity.items) - set(old)

        for item in new:
            await self._item_repository.add(item)

        for item in set(entity.items) - new:
            await self._item_repository.update(item)

        await self._item_repository.save_changes()

    async def delete(self, entity: User) -> None:
        await self._user_repository.delete(entity)
        for item in entity.items:
            await self._item_repository.delete(item)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
