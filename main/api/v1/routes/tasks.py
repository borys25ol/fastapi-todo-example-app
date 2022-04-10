from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_201_CREATED

from main.core.dependencies import (
    basic_security,
    get_current_active_user,
    get_current_task,
    get_current_user,
)
from main.db.tables import User
from main.schemas.response import Response
from main.schemas.tasks import Task, TaskInCreate, TaskInDB, TaskInUpdate
from main.services.tasks import TasksService

router = APIRouter(dependencies=[Depends(basic_security)])


@router.get("", response_model=Response[List[TaskInDB]])
def get_all_task(
    skip: int = 0,
    limit: int = 100,
    service: TasksService = Depends(),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    Retrieve all tasks.
    """
    tasks = service.get_all_owner_tasks(
        owner_id=current_user.id, skip=skip, limit=limit
    )
    return Response(data=tasks)


@router.get("/{task_id}", response_model=Response[TaskInDB])
def get_task(task: Task = Depends(get_current_task)) -> Response:
    """,
    Retrieve a task by `task_id`.
    """
    return Response(data=task)


@router.post("", response_model=Response[TaskInDB], status_code=HTTP_201_CREATED)
def create_task(
    task: TaskInCreate,
    service: TasksService = Depends(),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Create new task.
    """
    task = service.insert_task(task=task, owner_id=current_user.id)
    return Response(data=task, message="The task was created successfully")


@router.put("/{task_id}", response_model=Response[TaskInDB])
def update_task(
    task_in_update: TaskInUpdate,
    task: Task = Depends(get_current_task),
    service: TasksService = Depends(),
) -> Response:
    """
    Update task by `task_id`.
    """
    task = service.update_task(task=task, task_update=task_in_update)
    return Response(data=task, message="The task was updated successfully")


@router.delete("/{task_id}", response_model=Response[TaskInDB])
def delete_task(
    task: Task = Depends(get_current_task), service: TasksService = Depends()
) -> Response:
    """
    Delete task by `task_id`.
    """
    task = service.delete_task(task=task)
    return Response(data=task, message="The task was deleted successfully")
