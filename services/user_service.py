import aiosqlite
from models.user import User
from repositories.pet_repository  import PetRepository
from repositories.user_repository import UserRepository
from repositories.item_repository import ItemRepository


class UserService:
    def __init__(self, conn: aiosqlite.Connection, curs: aiosqlite.Cursor):
        self._connection = conn
        self._cursor = curs
        self._user_repository = UserRepository(conn, curs)
        self._item_repository = ItemRepository(conn, curs)
        self._pet_repository  = PetRepository(conn, curs)


    async def get_all(self):
        items = await self._item_repository.get_all()
        pets  = await self._pet_repository.get_all()
        users = await self._user_repository.get_all()

        for user in users:
            user.items = list(filter(lambda i: i.owner_id == user.id, items))
            user.pets  = list(filter(lambda p: p.owner_id == user.id, pets))

        return users


    async def get(self, id: int) -> User:
        items = await self._item_repository.get_all()
        items = list(filter(lambda i: i.owner_id == id, items))

        pets = await self._pet_repository.get_all()
        pets = list(filter(lambda p: p.owner_id == id, pets))

        entity = await self._user_repository.get(id)

        entity.items = items
        entity.pets = pets

        return entity

    async def add(self, entity: User) -> None:
        await self._user_repository.add(entity)

        for item in entity.items:
            await self._item_repository.add(item)

        for pet in entity.pets:
            await self._pet_repository.add(pet)

        await self._item_repository.save_changes()
        await self._user_repository.save_changes()

    async def update(self, entity: User) -> None:
        await self._user_repository.update(entity)
        items = await self._item_repository.get_all()
        pets  = await self._pet_repository.get_all()
        items = filter(lambda i: i.owner_id == entity.id, items)
        pets  = filter(lambda p: p.owner_id == entity.id, pets)

        new_items = set(entity.items) - set(items)
        new_pets  = set(entity.pets)  - set(pets)

        for item in items:
            if item in new_items:
                await self._item_repository.add(item)
            else:
                await self._item_repository.update(item)

        for pet in pets:
            if pet in new_pets:
                await self._pet_repository.add(pet)
            else:
                await self._pet_repository.update(pet)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
        await self._pet_repository.save_changes()

    async def delete(self, entity: User) -> None:
        await self._user_repository.delete(entity)
        for item in entity.items:
            await self._item_repository.delete(item)

        for pet in entity.pets:
            await self._pet_repository.delete(pet)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
        await self._pet_repository.save_changes()
