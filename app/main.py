import datetime
import os


from enum import Enum
from typing import Dict, List, Optional, Set

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class PrimaryKey:
    def __init__(self):
        self.id = 0

    def next(self):
        self.id += 1
        return self.id

    def current(self):
        return self.id


class Class(str, Enum):
    CHEMISTRY = "chemistry"
    COMPUTERSCIENCE = "computer science"
    LAW = "law"
    MEDICINE = "medicine"
    PHYSICS = "physics"

    @classmethod
    def all(self):
        return [c for c in self.__members__.values()]


class Student:
    def __init__(self, name, age):
        self.name: str = name
        self.age: int = age
        self.classes: Set[Class] = set()

    def add_class(self, class_name):
        self.classes.append(class_name)

    def remove_class(self, class_name: Class):
        self.classes.discard(class_name)


app = FastAPI()


students: Dict[PrimaryKey, Student] = dict()
key = PrimaryKey()


@app.get("/")
async def root():
    hostname: Optional[str] = os.uname().nodename
    return JSONResponse(
        content={
            "message": "Hello world",
            "hostname": hostname,
            "time": datetime.datetime.isoformat(datetime.datetime.now()),
        }
    )


class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    classes: List[Class]


@app.get("/students/find", response_model=StudentOut)
async def find_student(name: str) -> JSONResponse:
    for id, student in students.items():
        if student.name == name:
            return StudentOut(
                id=id, name=student.name, age=student.age, classes=student.classes
            )

    return JSONResponse(content={"message": "Student not found"}, status_code=404)


@app.get("/students/{id}", response_model=StudentOut)
async def get_student(id: int):
    student = students.get(id)
    if student is None:
        return JSONResponse(content={"message": "Student not found"}, status_code=404)

    return StudentOut(
        id=id, name=student.name, age=student.age, classes=student.classes
    )


@app.get("/students")
async def get_students():
    return students.items()


class StudentIn(BaseModel):
    name: str
    age: int
    classes: List[Class] | None = None


@app.post("/students", response_model=StudentOut)
async def create_student(studentIn: StudentIn):
    student = Student(name=studentIn.name, age=studentIn.age)

    if studentIn.classes is not None:
        for class_name in studentIn.classes:
            student.add_class(class_name)

    id = key.next()
    students[id] = student
    return StudentOut(
        id=id, name=student.name, age=student.age, classes=student.classes
    )


class ClassOut(BaseModel):
    name: str


@app.get("/courses")
async def get_courses():
    return Class.all()
