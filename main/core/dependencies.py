from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from main.core.exceptions import (
    InactiveUserAccountException,
    TaskNotFoundException,
    UserPermissionException,
)
from main.db.repositories.tasks import TasksRepository, get_tasks_repository
from main.models.task import Task
from main.models.user import User
from main.services.user import UserService

basic_security = HTTPBasic()


def get_current_user(
    user_service: UserService = Depends(),
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> User:
    """
    Return current user.
    """
    user = user_service.authenticate(
        username=credentials.username, password=credentials.password
    )
    return user


def get_current_task(
    task_id: str,
    repo: TasksRepository = Depends(get_tasks_repository),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Check if task with `task_id` exists in database.
    """
    task = repo.get(obj_id=task_id)
    if not task:
        raise TaskNotFoundException(
            message=f"Task with id `{task_id}` not found",
            status_code=HTTP_404_NOT_FOUND,
        )
    if task.owner_id != current_user.id:
        raise UserPermissionException(
            message="Not enough permissions", status_code=HTTP_403_FORBIDDEN
        )
    return task


def get_current_active_user(
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Return current active user.
    """
    if not user_service.check_is_active(user=current_user):
        raise InactiveUserAccountException(
            message="Inactive user", status_code=HTTP_400_BAD_REQUEST
        )
    return current_user
