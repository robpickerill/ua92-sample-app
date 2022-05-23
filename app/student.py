from enum import Enum

from typing import Set


class Module(str, Enum):
    CHEMISTRY = "chemistry"
    COMPUTERSCIENCE = "computer science"
    LAW = "law"
    MEDICINE = "medicine"
    PHYSICS = "physics"

    @classmethod
    def all(cls):
        return list(map(lambda m: m.value, cls))


class Student:
    def __init__(self, name, age):
        self.name: str = name
        self.age: int = age
        self.modules: Set[Module] = set()

    def add_class(self, class_name):
        self.classes.append(class_name)

    def remove_class(self, class_name: Module):
        self.classes.discard(class_name)
