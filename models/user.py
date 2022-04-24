from __future__ import annotations
import sqlite3
from models.item import Item


class User(object):
    def __init__(self, id: int, username: str, items: list[Item], experience: int, wallet: int, bank: int):
        self.__id       = id
        self.username   = username
        self.items      = items
        self.experience = experience
        self.wallet     = wallet
        self.bank       = bank

    @classmethod
    def new(cls, id: int, username: str) -> User:
        """create new users with this"""
        return cls(id, username, [], 0, 0, 0)

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
        return cls(data[0], data[1], [], data[2], data[3], data[4])

    # dunder methods
    def __str__(self):
        return f"({self.__id}) {self.username}"

    def __repr__(self):
        return f"<User id={self.__id} username={self.username} items={self.items}>"
