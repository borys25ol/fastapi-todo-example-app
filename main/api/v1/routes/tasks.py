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
from main.db.repositories.tasks import TasksRepository, get_tasks_repository
from main.models.task import Task
from main.models.user import User
from main.schemas.response import Response
from main.schemas.tasks import TaskInCreate, TaskInDB, TaskInUpdate, TasksInDelete

router = APIRouter(dependencies=[Depends(basic_security)])


@router.get("", response_model=Response[List[TaskInDB]])
def get_all_task(
    skip: int = 0,
    limit: int = 100,
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    Retrieve all tasks.
    """
    tasks = tasks_repo.get_all_by_owner(
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
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Create new task.
    """
    task = tasks_repo.create_with_owner(obj_create=task, owner_id=current_user.id)
    return Response(data=task, message="The task was created successfully")


@router.put("/{task_id}", response_model=Response[TaskInDB])
def update_task(
    task_in_update: TaskInUpdate,
    task: Task = Depends(get_current_task),
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
) -> Response:
    """
    Update task by `task_id`.
    """
    task = tasks_repo.update(obj=task, obj_update=task_in_update)
    return Response(data=task, message="The task was updated successfully")


@router.delete("/{task_id}", response_model=Response[TaskInDB])
def delete_task(
    task: Task = Depends(get_current_task),
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
) -> Response:
    """
    Delete task by `task_id`.
    """
    task = tasks_repo.delete(obj_id=task.id)
    return Response(data=task, message="The task was deleted successfully")


@router.delete("", response_model=Response[TasksInDelete])
def delete_tasks(
    tasks: TasksInDelete,
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Bulk delete tasks.
    """
    tasks = tasks_repo.delete_many_by_owner(obj_ids=tasks.ids, owner_id=current_user.id)
    return Response(
        data=TasksInDelete(ids=tasks), message="The tasks was deleted successfully"
    )
