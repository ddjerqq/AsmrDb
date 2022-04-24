import asyncio
from database import AsmrDb


async def main():
    db = await AsmrDb.new()
    users = await db.users.get_all()

    for user in users:
        print(user)
        for item in user.items:
            print(repr(item))


if __name__ == "__main__":
    asyncio.run(main())
