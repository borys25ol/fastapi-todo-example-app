from typing import List

from pydantic import BaseModel, Field, root_validator


class TaskBase(BaseModel):
    title: str = Field(..., title="Task title")
    done: bool = Field(..., title="Task finish state")


class Task(TaskBase):
    id: int


class TaskInDB(Task):
    class Config:
        orm_mode = True
        fields_order = ["id", "title", "done"]

    @root_validator
    def reorder(cls, values: dict) -> dict:
        return {field: values[field] for field in cls.Config.fields_order}


class TaskInCreate(BaseModel):
    title: str = Field(..., title="Task title")


class TaskInUpdate(TaskBase):
    ...


class TasksInDelete(BaseModel):
    ids: List[int]
