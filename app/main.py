import datetime
import os

from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models import StudentIn, StudentOut, ModuleOut
from app.student import Module, Student


class PrimaryKey:
    def __init__(self):
        self.id = 0

    def next(self):
        self.id += 1
        return self.id

    def current(self):
        return self.id


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


@app.get("/modules/{id}", response_model=ModuleOut)
async def get_student_modules(id: int):
    student = students.get(id)
    if student is None:
        return JSONResponse(content={"message": "Student not found"}, status_code=404)

    return ModuleOut(modules=student.modules)


@app.get("/modules", response_model=ModuleOut)
async def get_modules():
    return ModuleOut(modules=Module.all())
