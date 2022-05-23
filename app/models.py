from typing import List

from pydantic import BaseModel

from app.student import Module


class StudentIn(BaseModel):
    name: str
    age: int
    classes: List[Module] | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    classes: List[Module]


class ModuleOut(BaseModel):
    modules: List[str]
