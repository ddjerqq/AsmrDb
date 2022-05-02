import asyncio
from database import AsmrDb
from models.item import Item
from models.user import User


async def register_user_example(db: AsmrDb):
    print('register user example')
    alana = User.new(952416153450459166, "Alana")
    print(alana)

    djerq = User.new(725773984808960050, "ddjerqq")
    print(djerq)

    await db.users.add(alana)
    await db.users.add(djerq)

    print('added users to database')


async def give_user_items(db: AsmrDb):
    print('give user items example')
    user_id = 952416153450459166
    blue_gem = Item.new("blue_gem", user_id)
    print(blue_gem)

    user = await db.users.get(user_id)
    print(user)
    print(user.items)

    user.items.append(blue_gem)
    print(user.items)

    await db.users.update(user)
    print('user has been updated')


async def use_item(db: AsmrDb):
    print('use item example')
    user_id = 952416153450459166
    user = await db.users.get(user_id)
    print(user)
    print(user.items)

    blue_gem = next(i for i in user.items if i.type == "blue_gem")
    print(blue_gem)

    user.wallet += 10
    user.items.remove(blue_gem)
    print(user.items)

    await db.users.update(user)
    print('user has been updated')


async def main():
    db = await AsmrDb.new()

    await register_user_example(db)
    await give_user_items(db)
    await use_item(db)


if __name__ == "__main__":
    asyncio.run(main())
