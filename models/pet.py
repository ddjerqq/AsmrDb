from __future__ import annotations
import sqlite3
from models.id import Id


class Pet(object):
    # constructors
    def __init__(self, id: int, type: str, name: str | None, experience: int, owner_id: int | None):
        self.__id       = id
        self.__type     = type
        self.experience = experience
        self.name       = name
        self.__owner_id = owner_id

    @classmethod
    def new(cls, type: str, owner_id: int = None) -> Pet:
        """create new users with this"""
        id = Id.generate()
        return cls(id, type, None, 0, owner_id)

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

    # database methods
    @property
    def to_db(self) -> tuple:
        return self.__id, self.__type, self.name, self.experience, self.__owner_id

    @classmethod
    def from_db(cls, data: tuple | sqlite3.Row) -> Pet:
        return cls(*data)

    # dunder methods
    def __hash__(self):
        return hash(self.to_db)

    def __eq__(self, other: Pet):
        return isinstance(other, Pet) and self.__id == other.__id

    def __str__(self):
        return f"{self.__type}"

    def __repr__(self):
        return f"<Pet id={self.__id} type={self.__type}>"
