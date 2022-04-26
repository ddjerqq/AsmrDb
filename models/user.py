from __future__ import annotations
import sqlite3
from models.item import Item
from models.pet import Pet


class User(object):
    def __init__(self,
                 id: int,
                 username: str,
                 items: list[Item],
                 pets:  list[Pet],
                 experience: int,
                 wallet: int,
                 bank: int) -> None:
        self.__id       = id
        self.username   = username
        self.items      = items
        self.pets       = pets
        self.experience = experience
        self.wallet     = wallet
        self.bank       = bank

    @classmethod
    def new(cls, id: int, username: str) -> User:
        """create new users with this"""
        return cls(id, username, [], [], 0, 0, 0)

    # getters
    @property
    def id(self) -> int:
        return self.__id

    # database methods
    @property
    def to_db(self) -> tuple:
        return self.__id, self.username, self.experience, self.bank, self.wallet

    @classmethod
    def from_db(cls, data: tuple | sqlite3.Row) -> User:
        return cls(*data)

    # dunder methods
    def __hash__(self):
        return hash(self.to_db)

    def __eq__(self, other: User):
        return isinstance(other, User) and self.__id == other.__id

    def __str__(self):
        return f"({self.__id}) {self.username}"

    def __repr__(self):
        return f"<User id={self.__id} username={self.username} items={self.items}>"
