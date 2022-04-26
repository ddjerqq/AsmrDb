from __future__ import annotations
import sqlite3
import random
from models.id import Id


class Item(object):
    # classmethods
    @classmethod
    def _generate_rarity(cls):
        return random.random() ** 2

    # constructors
    def __init__(self, id: int, type: str, rarity: float, owner_id: int | None):
        self.__id        = id
        self.__type      = type
        self.__rarity    = rarity
        self.__owner_id  = owner_id

    @classmethod
    def new(cls, type: str, owner_id: int = None) -> Item:
        """create new users with this"""
        id = Id.generate()
        r  = cls._generate_rarity()
        return cls(id, type, r, owner_id)

    # getters
    @property
    def id(self) -> int:
        return self.__id

    @property
    def owner_id(self):
        return self.__owner_id

    @property
    def type(self):
        return self.__type

    @property
    def rarity(self):
        return self.__rarity

    # database methods
    @property
    def to_db(self) -> tuple:
        return self.__id, self.__type, self.__rarity, self.__owner_id

    @classmethod
    def from_db(cls, data: tuple | sqlite3.Row) -> Item:
        return cls(*data)

    # dunder methods
    def __hash__(self):
        return hash(self.to_db)

    def __eq__(self, other: Item):
        return isinstance(other, Item) and self.__id == other.__id

    def __str__(self):
        return f"{self.__type}"

    def __repr__(self):
        return f"<Item id={self.__id} type={self.__type}>"
